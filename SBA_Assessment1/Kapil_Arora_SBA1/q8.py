# Question 8: Order High-Priority Tasks
# Difficulty: Medium
# Topic: Python Sorting and Lambdas
#
# Problem Statement:
# A sprint board stores tasks with a priority and due day.
# Complete the function so it returns only the high-priority task titles,
# ordered by due day and then by title.
#
# Expected Output:
# ['Fix bug', 'Prepare demo', 'Write tests']

tasks = [
    {"title": "Write tests", "priority": "high", "due_day": 3},
    {"title": "Fix bug", "priority": "high", "due_day": 1},
    {"title": "Refactor CSS", "priority": "low", "due_day": 2},
    {"title": "Prepare demo", "priority": "high", "due_day": 2},
]


def high_priority_titles(tasks):
    filtered = [task for task in tasks if task["priority"] == "high"]
    ordered = sorted(filtered, key=lambda task: task["due_day"])
    return [task["title"] for task in ordered]


print(high_priority_titles(tasks))
