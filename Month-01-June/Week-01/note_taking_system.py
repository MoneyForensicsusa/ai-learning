def save_note(title, content):
    with open("notebook.txt", "a") as p:
        p.write(f"Note: {title}\n")
        p.write(f"{content}\n")
        p.write("\n")

def read_notes():
    with open("notebook.txt", "r") as p:
        notes = p.read()
        print(notes)

def count_notes():
    count = 0
    with open("notebook.txt", "r") as p:
        for line in p:
            if line.startswith("Note:"):
                count = count + 1
    return count

    
save_note("Azure", "AZ104")
save_note("Git", "Hub")
save_note("SQL", "Database")
read_notes()
total = count_notes()
print(f"Total notes: {total}")
