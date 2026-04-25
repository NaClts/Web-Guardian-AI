import json
import os
from llama_cpp import Llama, LlamaGrammar


CONTEXT_SIZE = 4096

SYSTEM_PROMPT = (
    "You are a Web Application Firewall security classifier.\n "
    "Task: Decide if an HTTP request is malicious or benign.\n "
    "Analyze only the given request.\n "
    "Focus on attack indicators (e.g. injection, traversal, deserialization, RCE, auth bypass).\n "
    "If uncertain, lean malicious.\n "
    "Return only one character:\n "
    "1 = malicious\n "
    "0 = benign\n "
    "Do not explain."
)

# This grammar restricts the model so that it can only respond with a single binary digit: 0 or 1
GRAMMAR = LlamaGrammar.from_string(r'''
root ::= "0" | "1"
''')


class LLMEngine:

    def __init__(self, model_path):
        self.llm = Llama(
            model_path = model_path,
            n_ctx = CONTEXT_SIZE,
        )

    async def predict_is_legitimate(self, request):
        request_dict = await self._request_to_dict(request)
        is_legitimate = self._llm_predict_is_legitimate(request_dict)
        return is_legitimate

    def _llm_predict_is_legitimate(self, request_dict):
        request_text = json.dumps(
            request_dict,
            ensure_ascii=False
        )[:CONTEXT_SIZE]

        response = self.llm.create_chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Analyze this HTTP request: {request_text}"},
            ],
            temperature=0.0, # Deterministic
            max_tokens=1,
            grammar=GRAMMAR,
        )

        text = response["choices"][0]["message"]["content"].strip()
        return True if text == "0" else False

    async def _request_to_dict(self, request):
        body = await request.body()
        data = body.decode("utf-8", errors="replace") if body else ""
        return {
            "method": request.method,
            "url": str(request.url),
            "data": data,
            # "headers": dict(request.headers),
        }
