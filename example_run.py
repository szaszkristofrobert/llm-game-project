from rag_pipeline import NPCPipeline


if __name__ == "__main__":
    pipeline = NPCPipeline()
    result = pipeline.npc_kor()
    print(result["decision"])
    print(result["response"])
