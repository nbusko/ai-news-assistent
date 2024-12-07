import os

import torch
from sentence_transformers import SentenceTransformer

from config import WEIGHTS_PATH, DEFAULT_MODEL


class Embedder:
    def __init__(self):
        """
        Initializes the Embedder class by creating an
        instance of the SentenceTransformer model and setting the device.
        """
        self.model = SentenceTransformer(
            WEIGHTS_PATH if os.path.exists(WEIGHTS_PATH) else DEFAULT_MODEL,
            # cache_folder=os.getenv("TRANSFORMERS_CACHE"),
            device="cuda" if torch.cuda.is_available() else "cpu",
            # device="mps" if torch.backends.mps.is_available() else "cpu"
        )

    def answer(self, query):
        """
        Generates the embedding of the input
        query using the SentenceTransformer model.

        Args:
        - query: The input query for which the
        embedding needs to be generated.

        Returns:
        - result: A dictionary containing the query
        embedding as a list of floating-point numbers.
        """
        # with torch.no_grad():
        emb = self.model.encode(query, convert_to_tensor=True, normalize_embeddings=True)

        result = {
            "query_embedding": [float(el) for el in torch.squeeze(emb)],
        }

        torch.cuda.empty_cache()

        return result


if __name__ == "__main__":
    emb = Embedder()

    r = emb.answer("Test input str")