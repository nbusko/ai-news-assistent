import os

import torch
from sentence_transformers import SentenceTransformer

from config import DEFAULT_MODEL


class Embedder:
    def __init__(self):
        """
        Initializes the Embedder class by creating an
        instance of the SentenceTransformer model and setting the device.
        """
        self.model = SentenceTransformer(
            (
                os.getenv("SPECIFIC_MODEL")
                if os.getenv("SPECIFIC_MODEL")
                else DEFAULT_MODEL
            ),
            device="cuda" if torch.cuda.is_available() else "cpu",
            cache_folder=os.getenv("TRANSFORMERS_CACHE"),
        )

    def answer(self, query):
        """
        Generates the embedding of the input
        query using the SentenceTransformer model.

        Args:
        - query list: The input query list for which the
        embeddings needs to be generated.

        Returns:
        - result: A dictionary containing the query
        embedding as a list of floating-point numbers.
        """

        emb = self.model.encode(
            query, convert_to_tensor=True, normalize_embeddings=True, batch_size=16
        )

        results = [
            {"query_embedding": [float(el) for el in torch.squeeze(embedding)]}
            for embedding in emb
        ]

        torch.cuda.empty_cache()

        return results


if __name__ == "__main__":
    emb = Embedder()

    r = emb.answer("Test input str")
