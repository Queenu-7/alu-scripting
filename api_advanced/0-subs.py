#!/usr/bin/python3
"""Query the Reddit API for subreddit subscriber counts."""

import requests


def number_of_subscribers(subreddit):
    """Return the number of subscribers for a given subreddit.

    If the subreddit is invalid, return 0.
    """
    if not subreddit or not isinstance(subreddit, str):
        return 0

    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {'User-Agent': 'My-User-Agent'}

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)

        if response.status_code == 200:
            data = response.json()
            return data.get('data', {}).get('subscribers', 0)
        else:
            return 0
    except Exception:
        return 0
