from datetime import datetime
from fastapi import FastAPI, Request, Response
from helper__ml_engine import MLEngine
from helper__llm_engine import LLMEngine
from helper__segment_http_dict_into_words import segment_http_dict_into_words
from helper__stopwatch import Stopwatch
from pathlib import Path

AVAILABLE_MODES = ("ML_WITH_LLM", "ML-ONLY", "LLM-ONLY") # DO NOT EDIT THIS LINE

################################################################
########################### Configs ############################
################################################################

MODE = AVAILABLE_MODES[0]

FASTTEXT_MODEL_PATH = r"models/fasttext3_unsupervised_segmented_train_csic_ecml-pkdd.bin"
CLASSIFIER_PATH = r"models/clf_fasttext3_segmented_final_train_0.05-wcp_csic_ecml-pkdd.joblib"
LLM_MODEL_PATH = r"models/Phi-3.5-mini-instruct-Q4_K_M.gguf"

ML_PROB_THRESHOLD = 0.6

DEBUG = False

################################################################
########################## Constants ###########################
################################################################

if ( MODE == AVAILABLE_MODES[0] ) or ( MODE == AVAILABLE_MODES[1] ):
    ML_ENGINE = MLEngine(
        fasttext_model_path = FASTTEXT_MODEL_PATH,
        classifier_path = CLASSIFIER_PATH
    )

if ( MODE == AVAILABLE_MODES[0] ) or ( MODE == AVAILABLE_MODES[2] ):
    LLM_ENGINE = LLMEngine(
        model_path = LLM_MODEL_PATH
    )

STOPWATCH_OUTPUT_FILENAME = "auth_service_py_elapsed_time_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
FILE_PATH = Path(__file__).resolve()
FILE_DIR = FILE_PATH.parent
STOPWATCH_OUTPUT_DIR = FILE_DIR / "elapsed_time"
STOPWATCH_OUTPUT_DIR.mkdir(parents=True, exist_ok=True) # create if not exists
STOPWATCH_OUTPUT_PATH = STOPWATCH_OUTPUT_DIR / STOPWATCH_OUTPUT_FILENAME

################################################################
####################### Helper Functions #######################
################################################################

async def is_authenticated(request: Request) -> bool:

    # "ML_WITH_LLM"
    if MODE == AVAILABLE_MODES[0]:
        legit_prob, mal_prob = await ML_ENGINE.predict_request_proba(request)

        if max(legit_prob, mal_prob) < ML_PROB_THRESHOLD:
            is_legitimate = await LLM_ENGINE.predict_is_legitimate(request)
        else:
            is_legitimate = (legit_prob > mal_prob)

    # "ML-ONLY"
    elif MODE == AVAILABLE_MODES[1]:
        legit_prob, mal_prob = await ML_ENGINE.predict_request_proba(request)
        is_legitimate = (legit_prob > mal_prob)

    # "LLM-ONLY"
    elif MODE == AVAILABLE_MODES[2]:
        is_legitimate = await LLM_ENGINE.predict_is_legitimate(request)

    return is_legitimate

################################################################
############################# Main #############################
################################################################

app = FastAPI()

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
async def catch_all(request: Request, full_path: str):

    if DEBUG:
        stopwatch = Stopwatch()
        stopwatch.start()

    authenticated = await is_authenticated(request)

    if DEBUG:
        stopwatch.stop()
        stopwatch.write(STOPWATCH_OUTPUT_PATH)

    if authenticated:
        return Response(status_code=200)
    return Response(status_code=403)
