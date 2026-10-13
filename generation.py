from google import genai
client= genai.Client()
def generate_response(prompt):
      response=client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
      )
      return response.text