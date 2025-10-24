#!/usr/bin/python3
"""
Recursive function that queries the Reddit API
and returns a list containing
the titles of all hot articles for a given subreddit.
If no results are found for the given subreddit,
the function should return None.
"""
import requests


def recurse(subreddit, hot_list=None, after=None):
    """
    Recursively queries Reddit API to get all hot articles from a subreddit

    Args:
        subreddit (str): The subreddit to search
        hot_list (list): List to accumulate article titles
        after (str): Pagination token for next page

    Returns:
        list: List of hot article titles, or None if subreddit is invalid
    """
    # Initialize hot_list if not provided
    if hot_list is None:
        hot_list = []

    # Base URL for Reddit API
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)

    # Set headers to avoid redirects and identify our bot
    headers = {
        'User-Agent': 'python:reddit_recursive_scraper:v1.0'
    }

    # Add pagination parameter if we have an 'after' token
    params = {'limit': 100}
    if after:
        params['after'] = after

    # Make the API request - don't follow redirects automatically
    response = requests.get(
        url,
        headers=headers,
        params=params,
        allow_redirects=False
    )

    # If we get a redirect or any non-200 status, subreddit doesn't exist
    if response.status_code != 200:
        return None

    # Parse the JSON response
    data = response.json()

    # Extract posts from the current page
    posts = data['data']['children']

    # If no posts found and this is the first page, return None
    if not posts and after is None:
        return None

    # Add titles from current page to our list
    for post in posts:
        hot_list.append(post['data']['title'])

    # Get the pagination token for next page
    next_after = data['data']['after']

    # If there's a next page, make recursive call
    if next_after:
        return recurse(subreddit, hot_list, next_after)
    else:
        # No more pages, return the accumulated list
        return hot_list
