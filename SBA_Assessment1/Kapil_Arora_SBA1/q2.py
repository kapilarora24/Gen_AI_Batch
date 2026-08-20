# Question 2: Count Completed Tasks
# Difficulty: Easy
# Topic: Python Loops and Dictionaries
#
# Problem Statement:
# A project tracker stores tasks as dictionaries.
# Complete the function so it counts how many tasks are marked as done.
#
# Expected Output:
# 2

tasks = [
    {"title": "Design login page", "done": True},
    {"title": "Write API docs", "done": False},
    {"title": "Deploy staging build", "done": True},
]


def count_completed(tasks):
    completed = 0
    for task in tasks:
        if task["done"]:
            completed += 1
    return completed


print(count_completed(tasks))
