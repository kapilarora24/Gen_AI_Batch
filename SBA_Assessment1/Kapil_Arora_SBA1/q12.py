# Question 12: Build an Active User Query
# Difficulty: Medium
# Topic: PostgreSQL SELECT Query
#
# Problem Statement:
# Complete the SQL query so it selects the employee id and full name,
# filters active users by department, and sorts the results by full name.
#
# Expected Output:
# SELECT id, full_name FROM employees WHERE department = %s AND is_active = TRUE ORDER BY full_name ASC;
# ('Sales',)


def build_active_user_query(department):
    query = (
        "SELECT id, full_name FROM employees "
        "WHERE department = %s AND full_name "
        "ORDER BY full_name ASC;"
    )
    return query, (department,)


sql, params = build_active_user_query("Sales")
print(sql)
print(params)
