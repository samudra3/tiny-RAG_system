def chunking(text,chunk_size,overlap):
      paragraphs= text.split("\n\n")
      chunks=[]
      current_chunk=""
      for paragraph in paragraphs:
            paragraph=paragraph.strip()
            if not paragraph:
                  continue
            if len(paragraph)+len(current_chunk)+2<=chunk_size:
                  if current_chunk:
                        current_chunk+="\n\n"

                  current_chunk+=paragraph

            else:
                  if current_chunk:
                        chunks.append(current_chunk)
                  current_chunk=paragraph

      if current_chunk:
            chunks.append(current_chunk)


      return chunks