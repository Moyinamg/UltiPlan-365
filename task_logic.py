from priority import calculate_priority

importance_rank = {
    "High": 3,
    "Medium": 2,
    "Low": 1
}

difficulty_rank = {
    "Hard": 3,
    "Medium": 2,
    "Easy": 1
}

def create_task(
    course,
    task_name,
    deadline,
    importance,
    difficulty,
    estimated_minutes
):
    task = {
        "course": course,
        "task_name": task_name,
        "deadline": deadline,
        "importance": importance,
        "difficulty": difficulty,
        "estimated_minutes": estimated_minutes
    }

    task["priority_score"] = calculate_priority(task)

    return task

def sort_tasks(tasks):
    tasks.sort(
        key=lambda task: (
        -task["priority_score"],
        task["deadline"],
        -importance_rank[task["importance"]],
        -difficulty_rank[task["difficulty"]]
        )
    )
    return tasks