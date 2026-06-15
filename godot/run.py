import sys
sys.path.append('../')
from rag_pipeline import NPCPipeline

if __name__ == "__main__":
    pipeline = NPCPipeline()
    result = pipeline.npc_turn()
    
    myfile = "response.txt"

    with open(myfile, 'w') as filetowrite:
        filetowrite.write(result["response"])
