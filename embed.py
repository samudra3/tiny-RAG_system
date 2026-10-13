from google import genai


def embed_text(text):
      client= genai.Client()

      response= client.models.embed_content(
            model="gemini-embedding-2",
            contents=text
      )

      return response.embeddings[0].values