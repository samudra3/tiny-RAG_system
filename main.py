from chunk import chunking
from pathlib import Path
from embed import embed_text
from dotenv import load_dotenv
from retrieval import retrieval
from prompt_builder import get_prompt
load_dotenv()
from generation import generate_response
from chroma_test import collection
directory_path= Path("documents/remote-work.txt")

text= directory_path.read_text()
example="this is for the example embed me"
paragraphs_chunks= chunking(text,chunk_size=100,overlap=20)
embed_chunks=[]

def embedding(paragraphs_chunks):
      for index,chunk in enumerate(paragraphs_chunks):
           vector=embed_text(chunk)
           embed_chunks.append({
                 "index":index,
                 "vector":vector,
                 "context":chunk,
                 "source":"remote-work.txt"
           })
embedding(paragraphs_chunks)
# for index,data in enumerate(embed_chunks):
#       print(f'---{index}---')
#       print(data["context"])
#       print(len(data["vector"]))
#       print('-------------')
query= "How many days can I work from home?"
# relevant_chunks=retrieval(query,embed_chunks)
# required_prompt= get_prompt(query,relevant_chunks)
# answer= generate_response(required_prompt)
# print(answer)
# for i,chunk in enumerate(embed_chunks):
#       collection.add(
#             ids=[f'chunk id: {i}'],
#             documents=[chunk["context"]],
#             metadatas=[{"source":chunk["source"]}],
#             embeddings=[chunk["vector"]]
#       )
relevant_chunks=retrieval(query,2)
prompt= get_prompt(query,relevant_chunks["documents"][0])
print(prompt)