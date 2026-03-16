from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def review_code(diff: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior software engineer performing a thorough code review. Be precise, constructive and developer-friendly."
                },
                {
                    "role": "user",
                    "content": f"""Review the following code diff and provide structured feedback.

Focus on:
- Bugs or logical errors
- Security vulnerabilities
- Code quality and best practices
- Performance improvements

For each issue found, mention:
- What the issue is
- Why it is a problem
- How to fix it

If no issues found in a section, write "No issues found."

Code diff:
{diff}"""
                }
            ],
            max_tokens=1024,
            temperature=0.3
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"LLM review failed: {e}")
        return "Code review could not be completed due to an internal error."