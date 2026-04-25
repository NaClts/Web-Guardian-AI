import fasttext
import joblib
import numpy as np
from helper__segment_http_dict_into_words import segment_http_dict_into_words


class MLEngine:

    def __init__(self, fasttext_model_path, classifier_path):
        self.fasttext_model = fasttext.load_model(fasttext_model_path)
        self.classifier = joblib.load(classifier_path)
    
    async def predict_request_proba(self, request):
        request_dict = await self._request_to_dict(request)

        # Unsqueeze
        X = [request_dict]

        X_tokenized = self._tokenize(X)
        X_vectorized = self._fasttext_vectorize(X_tokenized)
        probs = self.classifier.predict_proba(X_vectorized)
        legit_prob, mal_prob = probs[0]
        return legit_prob, mal_prob

    async def _request_to_dict(self, request):
        body = await request.body()
        data = body.decode("utf-8", errors="replace") if body else ""
        return {
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "data": str(data)
        }

    def _tokenize(self, X):
        return [ ' '.join(segment_http_dict_into_words(request_dict)) for request_dict in X ]
    
    def _fasttext_vectorize(self, X):
        X_vectorized = [ self.fasttext_model.get_sentence_vector(text) for text in X ]
        X_vectorized = np.array(X_vectorized, dtype=np.float32)
        return X_vectorized