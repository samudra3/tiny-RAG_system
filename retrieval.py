from embed import embed_text
import numpy as np
from chroma_test import collection

def cosine_similarity(vector_a,vector_b):
      a = np.array(vector_a)
      b = np.array(vector_b)

      return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))

def retrieval(query,n_chunks=2):
      query_vector=embed_text(query)
      results= collection.query(query_embeddings=[query_vector],
                                n_results=n_chunks)

      # for i in embed_chunks:
      #     score= cosine_similarity(query_vector,i["vector"])
      #     results.append({
      #       "source":i["source"],
      #       "context":i["context"],
      #       "score":score,
      #       "chunk_id":i["index"]

      # })
      # results=sorted(results,
      #          key=lambda item:item["score"],
      #          reverse=True
      #          )
      return results