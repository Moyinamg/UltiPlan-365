def create_study_plan(tasks, available_minutes):
    study_plan = []
    remaining_minutes = available_minutes
    
    #Tasks are already stored from highest priority
    for task in tasks:
        if remaining_minutes <= 0:
            break

        estimated = task["estimated_minutes"]


        #Determine whether the task can be completed today.
        if estimated <= remaining_minutes:
            allocated = estimated
            status = "Complete Today"
        
        # Only including part of the tasks that fits today
        else:
            allocated = remaining_minutes
            status = "Continue Tomorrow"

        study_plan.append({
            "course": task["course"],
            "task_name": task["task_name"],
            "allocated_minutes": allocated,
            "estimated_minutes": estimated,
            "remaining_minutes": estimated - allocated,
            "status": status
        })

        remaining_minutes -= allocated

    return study_plan