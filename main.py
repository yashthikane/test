import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException
from github_client import get_pr_diff, post_review_comment
from gemini_client import review_code
from config import WEBHOOK_SECRET
# from llm_client import review_code

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "AI Code Reviewer is running"}

@app.post("/webhook/github")
async def github_webhook(request: Request):
    payload = await request.json()

    action = payload.get("action")
    if action not in ["opened", "synchronize"]:
        return {"message": "Event ignored"}

    pr = payload.get("pull_request", {})
    repo = payload.get("repository", {})

    pr_number = pr.get("number")
    repo_full_name = repo.get("full_name")
    pr_title = pr.get("title")

    print(f"PR #{pr_number} - {pr_title} in {repo_full_name}")

    diff = get_pr_diff(repo_full_name, pr_number)
    if not diff:
        return {"message": "Could not fetch diff"}

    print("Diff fetched, sending to Gemini...")
    review = review_code(diff)

    comment_body = f"## AI Code Review\n\n{review}"
    status = post_review_comment(repo_full_name, pr_number, comment_body)

    print(f"Comment posted with status: {status}")
    return {"message": "Review posted successfully"}