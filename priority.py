from datetime import datetime, date

#Creating function that receives one task dictionary
def calculate_priority(task):
    deadline_date = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
    days_left = (deadline_date - date.today()).days
    
    # Priority Score logic
    score = 0

    if days_left == 0:
        score += 50
    elif days_left <= 2:
        score += 40
    elif days_left == 5:
        score += 30
    elif days_left == 7:
        score += 20
    else:
        score += 10
    
    if task["importance"] == "High":
        score += 30
    elif task["importance"] == "Medium":
        score += 20
    else:
        score += 10
    
    if task["difficulty"] == "Hard":
        score += 20
    elif task["difficulty"] == "Medium":
        score += 10
    else:
        score += 5
    
    return score
    