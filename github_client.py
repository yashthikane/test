import requests
from config import GITHUB_TOKEN

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_pr_diff(repo_full_name: str, pr_number: int) -> str:
    url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}"
    headers = {**HEADERS, "Accept": "application/vnd.github.v3.diff"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return ""

def post_review_comment(repo_full_name: str, pr_number: int, body: str):
    url = f"https://api.github.com/repos/{repo_full_name}/issues/{pr_number}/comments"
    payload = {"body": body}
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.status_code