def greet(name):
    message = f"Hello {name}, welcome to AI Engineering."
    return message

def add(a, b):
    return a + b

def study_feedback(hours):
    if hours >= 2:
        return "strong session - great work"
    elif hours >= 1:
        return "Decent - aim for 2 hours tomorrow"
    else:
        return "Short session - plan more for tomorrow"
result = greet("bob")
print(result)
total = add(15, 27)
print(total)
feedback = study_feedback(1.5)
print(feedback)        

def hours_to_minutes(hours):
    return hours * 60
minutes = hours_to_minutes(2)
print(f"{minutes} minutes")

def full_name(first, last):
    return first + " " + last
full_name = full_name("Wonderful", "Eyeh")
print(full_name)

def is_strong_password(password):
    if len(password) > 8:
        return "true"
    else:
        return "false"
password = is_strong_password("Wonder2")
print(password)

def plan_hours(daily, weeks):
    return daily * 7 * weeks
plan_hours = plan_hours(2, 10)
print(plan_hours)

def full_greeting(name, role):
    return f"Hello {name}, welcome to {role}"

greeting = full_greeting("Wonderful", "AI Engineering")
print(greeting)