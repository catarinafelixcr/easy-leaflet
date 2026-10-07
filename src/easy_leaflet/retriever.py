import numpy as np
from sentence_transformers import SentenceTransformer


# The worker that finds the best chunks for a question
class Retriever:

    def __init__(self, model_name="intfloat/multilingual-e5-small"):
        self.model = SentenceTransformer(model_name)
        self.chunks = []
        self.vectors = None

    def index(self, chunks):
        # Turn every chunk into a vector (done one time)
        self.chunks = chunks
        texts = []
        for chunk in chunks:
            texts.append("passage: " + chunk.text)
        
        self.vectors = self.model.encode(texts, normalize_embeddings=True)

    def search(self, question, k=4, leaflet_name=None):
        # Return the k chunks that are closest to the question
        query = self.model.encode("query: " + question, normalize_embeddings=True)

        # One score per chunk: how similar it is to the question
        scores = self.vectors @ query

        # If a medicine was chosen, chunks from other leaflets cannot win
        if leaflet_name is not None:
            for i, chunk in enumerate(self.chunks):
                if chunk.leaflet_name != leaflet_name:
                    scores[i] = -np.inf

        # Positions of the k highest scores, best first
        positions = np.argsort(scores)[::-1][:k]

        results = []
        for i in positions:
            results.append(self.chunks[i])
        return results