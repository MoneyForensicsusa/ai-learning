#lists
skills = ["python", "Git", "SQL", "Azure", "AI"]
skills.append("Docker")
print(skills[0])
print(skills[2])
print(len(skills))
for skill in skills:
    print(f" > {skill}")
#dictionaries
profile = {
    "name": "Wonderful",
    "track": "AI Engineering",
    "month": "June",
    "study_hours": 2
}
profile["city"] = "Austin"
print(profile)
print(profile["study_hours"] * 7)
for key, value in profile.items():
    print(f"{key}:{value}")