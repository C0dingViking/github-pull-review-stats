import os
import requests
import json
from collections import Counter
from pathlib import Path
from dotenv import load_dotenv
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

ENV_PATH = Path("config/.env")
load_dotenv(dotenv_path=ENV_PATH)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN not found in config/.env")


CONFIG_PATH = "config/config.json"

try:
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
        OWNER = config["owner"]
        REPO = config["repo"]
        if not OWNER or not REPO:
            raise RuntimeError("owner and repo must be set in config.json")
except FileNotFoundError:
    raise RuntimeError("config.json not found")
except KeyError as e:
    raise RuntimeError(f"Missing key in config.json: {e}")

API_BASE = "https://api.github.com"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

EXCLUDED_LOGINS = {
    "github-copilot",
    "copilot[bot]"
}

VALID_REVIEW_STATES = {
    "APPROVED",
    "REQUEST_CHANGES"
}

def get_all_pages(url, params=None):
    results = []

    while url:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()

        results.extend(response.json())
        url = response.links.get("next", {}).get("url")
        params = None

    return results

def fetch_review_counts():
    counter = Counter()

    pulls_url = f"{API_BASE}/repos/{OWNER}/{REPO}/pulls"
    pulls = get_all_pages(
        pulls_url,
        params={"state": "all", "per_page": 100}
    )

    print(f"Found {len(pulls)} pull requests")

    for pr in pulls:
        pr_number = pr["number"]
        reviews_url = f"{API_BASE}/repos/{OWNER}/{REPO}/pulls/{pr_number}/reviews"

        reviews = get_all_pages(
            reviews_url,
            params={"per_page": 100}
        )

        for review in reviews:
            user = review.get("user")

            if not user:
                continue
            
            login = user["login"]

            if login in EXCLUDED_LOGINS or user.get("type") == "Bot":
                continue

            if review["state"] not in VALID_REVIEW_STATES:
                continue

            counter[user["login"]] += 1

    return counter

def plot_reviews(counter):
    users = list(counter.keys())
    counts = list(counter.values())

    plt.figure(dpi=150)
    plt.bar(
        users, 
        counts,
        width=0.6,
        color="#9626e6")
    plt.xlabel("Reviewer")
    plt.ylabel("Number of Reviews")
    plt.title("Pull Request Reviews per Person")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    review_counts = fetch_review_counts()

    print("\nReview counts:")
    for user, count in review_counts.most_common():
        print(f"{user}: {count}")

    plot_reviews(review_counts)
