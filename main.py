import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from github_client import get_pr_diff, post_review_comment
from llm_client import review_code
from config import WEBHOOK_SECRET

app = FastAPI()

def verify_signature(payload: bytes, signature: str) -> bool:
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)

def process_pr_review(repo_full_name: str, pr_number: int, pr_title: str):
    print(f"Processing PR #{pr_number} - {pr_title} in {repo_full_name}")

    diff = get_pr_diff(repo_full_name, pr_number)
    if not diff:
        print(f"Could not fetch diff for PR #{pr_number}")
        return

    print(f"Diff fetched ({len(diff)} chars), sending to LLM...")
    review = review_code(diff)

    comment_body = f"## AI Code Review\n\n{review}"
    status = post_review_comment(repo_full_name, pr_number, comment_body)
    print(f"Comment posted with status: {status}")

@app.get("/")
def health_check():
    return {"status": "AI Code Reviewer is running"}

@app.post("/webhook/github")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    payload_bytes = await request.body()
    signature = request.headers.get("X-Hub-Signature-256", "")

    if signature and not verify_signature(payload_bytes, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()
    action = payload.get("action")

    if action not in ["opened", "synchronize"]:
        return {"message": f"Event ignored: {action}"}

    pr = payload.get("pull_request", {})
    repo = payload.get("repository", {})

    pr_number = pr.get("number")
    repo_full_name = repo.get("full_name")
    pr_title = pr.get("title")

    background_tasks.add_task(
        process_pr_review,
        repo_full_name,
        pr_number,
        pr_title
    )

    return {"message": "Review started"}