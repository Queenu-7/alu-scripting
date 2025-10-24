#!/usr/bin/python3
"""
Recursive function that queries the Reddit API, parses the title of all hot
articles, and prints a sorted count of given keywords
"""
import requests


def count_words(subreddit, word_list, after=None, word_count=None):
    """
    Recursively counts keywords in hot article titles from a subreddit

    Args:
        subreddit (str): The subreddit to search
        word_list (list): List of keywords to count
        after (str): Pagination token for next page
        word_count (dict): Dictionary to accumulate word counts

    Returns:
        None: Results are printed to stdout
    """
    # Initialize word_count dictionary on first call
    if word_count is None:
        word_count = {}
        # Convert word_list to lowercase and initialize counts
        for word in word_list:
            word_lower = word.lower()
            word_count[word_lower] = word_count.get(word_lower, 0)

    # Base URL for Reddit API
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)

    # Set headers
    headers = {
        'User-Agent': 'python:reddit_keyword_counter:v1.0'
    }

    # Add pagination parameter if we have an 'after' token
    params = {'limit': 100}
    if after:
        params['after'] = after

    # Make the API request - don't follow redirects
    response = requests.get(
        url,
        headers=headers,
        params=params,
        allow_redirects=False
    )

    # If subreddit is invalid, return without printing
    if response.status_code != 200:
        return

    # Parse the JSON response
    data = response.json()
    posts = data['data']['children']

    # Process titles from current page
    for post in posts:
        title = post['data']['title']
        # Split title into words and count matches
        words_in_title = title.split()
        for title_word in words_in_title:
            # Clean the word and convert to lowercase
            clean_word = ''.join(
                char for char in title_word if char.isalnum()
            ).lower()
            # Check if this clean word matches any of our keywords
            if clean_word in word_count:
                word_count[clean_word] += 1

    # Get the pagination token for next page
    next_after = data['data']['after']

    # If there's a next page, make recursive call
    if next_after:
        return count_words(subreddit, word_list, next_after, word_count)
    else:
        # No more pages - process and print results
        print_results(word_count)


def print_results(word_count):
    """
    Print the word counts in sorted order

    Args:
        word_count (dict): Dictionary of word counts
    """
    # Filter out words with zero counts
    filtered_counts = [
        (word, count) for word, count in word_count.items() if count > 0
    ]

    # Sort by count (descending) and then by word (ascending)
    sorted_counts = sorted(filtered_counts, key=lambda x: (-x[1], x[0]))

    # Print results
    for word, count in sorted_counts:
        print("{}: {}".format(word, count))
