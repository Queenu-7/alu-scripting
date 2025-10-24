#!/usr/bin/python3
"""Print the titles of the first 10 hot posts for a given subreddit."""

import requests


def top_ten(subreddit):
    """Query Reddit API and print the first 10 hot post titles."""
    if subreddit is None or not isinstance(subreddit, str):
        print(None)
        return

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "ALU-Reddit-Task/0.1"}
    params = {"limit": 10}

    try:
        response = requests.get(
            url, headers=headers, params=params,
            allow_redirects=False, timeout=10
        )

        # If subreddit invalid or redirect → print None
        if response.status_code != 200:
            print(None)
            return

        data = response.json().get("data")
        if not data or "children" not in data:
            print(None)
            return

        posts = data.get("children")
        if not posts:
            print(None)
            return

        printed = False
        for post in posts[:10]:
            title = post.get("data", {}).get("title")
            if title:
                print(title)
                printed = True

        # Handle sandbox (no Reddit access) – ensure at least some output
        if not printed:
            print("None")

    except Exception:
        print(None)
