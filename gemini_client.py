from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def review_code(diff: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""You are an expert code reviewer. Review the following code diff and provide feedback.

Focus on:
- Bugs or logical errors
- Security issues
- Code quality and best practices
- Performance improvements

Format your response clearly with sections.
Keep it concise and developer-friendly.

Code diff:
{diff}"""
            }
        ],
        max_tokens=1024
    )
    return response.choices[0].message.content