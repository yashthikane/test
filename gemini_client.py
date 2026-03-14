from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def review_code(diff: str) -> str:
    prompt = f"""
You are an expert code reviewer. Review the following code diff and provide feedback.

Focus on:
- Bugs or logical errors
- Security issues
- Code quality and best practices
- Performance improvements

Format your response clearly with sections.
Keep it concise and developer-friendly.

Code diff:
{diff}
"""
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    return response.text
