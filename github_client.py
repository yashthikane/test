import requests
from config import GITHUB_TOKEN

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

MAX_DIFF_SIZE = 10000

def get_pr_diff(repo_full_name: str, pr_number: int) -> str:
    try:
        url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}"
        headers = {**HEADERS, "Accept": "application/vnd.github.v3.diff"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            diff = response.text
            if len(diff) > MAX_DIFF_SIZE:
                print(f"Diff too large ({len(diff)} chars), truncating...")
                return diff[:MAX_DIFF_SIZE] + "\n... [diff truncated due to size]"
            return diff

        print(f"Failed to fetch diff: {response.status_code}")
        return ""

    except Exception as e:
        print(f"Error fetching diff: {e}")
        return ""

def post_review_comment(repo_full_name: str, pr_number: int, body: str) -> int:
    try:
        url = f"https://api.github.com/repos/{repo_full_name}/issues/{pr_number}/comments"
        payload = {"body": body}
        response = requests.post(url, headers=HEADERS, json=payload, timeout=10)
        return response.status_code

    except Exception as e:
        print(f"Error posting comment: {e}")
        return 500