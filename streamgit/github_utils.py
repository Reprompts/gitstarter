from github import Github, GithubException
from .config import get_github_token

def get_github_client():
    token = get_github_token()
    if not token:
        raise ValueError("GitHub token required for this action")
    return Github(token)

def create_remote_repo(name, private=True):
    gh = get_github_client()
    user = gh.get_user()
    try:
        repo = user.create_repo(name, private=private)
        return {"url": repo.clone_url, "success": True}
    except GithubException as e:
        return {"error": e.data.get("message"), "success": False}

def list_pull_requests(owner, repo):
    gh = get_github_client()
    return gh.get_repo(f"{owner}/{repo}").get_pulls()

def create_pull_request(owner, repo, title, body, head, base="main"):
    gh = get_github_client()
    try:
        pr = gh.get_repo(f"{owner}/{repo}").create_pull(
            title=title, body=body, head=head, base=base
        )
        return {"url": pr.html_url, "success": True}
    except GithubException as e:
        return {"error": e.data.get("message"), "success": False}
