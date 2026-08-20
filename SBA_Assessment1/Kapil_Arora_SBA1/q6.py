# Question 6: Collect Unique Tags
# Difficulty: Easy
# Topic: Python Data Structures
#
# Problem Statement:
# A content platform stores tags for each post.
# Complete the function so it returns a sorted list of unique tags across all posts.
#
# Expected Output:
# ['fastapi', 'genai', 'postgres', 'python']

posts = [
    {"title": "API Basics", "tags": ["python", "fastapi"]},
    {"title": "Prompt Design", "tags": ["genai", "python"]},
    {"title": "SQL Joins", "tags": ["postgres", "python"]},
]


def unique_tags(posts):
    return sorted({tag for post in posts for tag in post["tags"]})


print(unique_tags(posts))
