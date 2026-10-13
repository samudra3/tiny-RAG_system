
def get_prompt(question,relevant_chunks):
      prompt="you have to answer using the provided context\n\ncontext:"
      for chunks in relevant_chunks:
            prompt+=f'\n{chunks}'
      prompt+=f'\nQuestion: \n{question}\n'
      prompt+="\n answer only using provided context"
      return prompt