import chromadb
from chromadb.config import Settings


class FinancialSituationMemory:
    def __init__(self, name, config):
        self.chroma_client = chromadb.Client(Settings(allow_reset=True))
        self.situation_collection = self.chroma_client.get_or_create_collection(name=name)

    def add_situations(self, situations_and_advice):
        """Add financial situations and their corresponding advice."""
        offset = self.situation_collection.count()
        situations, advice, ids = [], [], []
        for i, (situation, recommendation) in enumerate(situations_and_advice):
            situations.append(situation)
            advice.append(recommendation)
            ids.append(str(offset + i))
        self.situation_collection.add(
            documents=situations,
            metadatas=[{"recommendation": rec} for rec in advice],
            ids=ids,
        )

    def get_memories(self, current_situation, n_matches=1):
        """Find matching recommendations using ChromaDB default embedding."""
        if self.situation_collection.count() == 0:
            return []
        results = self.situation_collection.query(
            query_texts=[current_situation],
            n_results=min(n_matches, self.situation_collection.count()),
            include=["metadatas", "documents", "distances"],
        )
        matched_results = []
        for i in range(len(results["documents"][0])):
            matched_results.append({
                "matched_situation": results["documents"][0][i],
                "recommendation": results["metadatas"][0][i]["recommendation"],
                "similarity_score": 1 - results["distances"][0][i],
            })
        return matched_results
