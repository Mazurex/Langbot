import requests
import re


def latest_github_version(github_repo: str) -> str:
    """Returns the latest github version"""
    response = requests.get(f"https://api.github.com/repos/{github_repo}/commits")

    if response.status_code == 200:
        for commit in response.json():
            version = commit["commit"]["message"].strip().split("\n")[0]
            if re.compile(r"^\d+\.\d+\.\d+$").match(version):
                return version
    return "Unknown"
