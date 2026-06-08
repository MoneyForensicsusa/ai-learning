#dictionary
course_summary = {
    "month_name": "June",
    "week_number": 1,
    "topic": "Python",
    "planned_hours": 12
}
#list
concepts = ["Azure", "SQL", "Git", "AI"]
print(f"In the month of {course_summary["month_name"]}, week number {course_summary["week_number"]}, I am studying {course_summary["topic"]}.")
for concept in concepts:
    print(f"> {concept}")