# Write a filr
with open("my_notes.txt", "w") as f:
    f.write("Day 7: Learning file handling\n")
    f.write("Files let programs remember infirmation\n")
    f.write("This is the third line")

# Read a file
with open("my_notes.txt", "r") as f:
    content = f.read()
    print(content)

# Append a file
with open("my_notes.txt", "a") as f:
    f.write("\nThis line was added later.")

#read line by line
with open("my_notes.txt", "r") as f:
    for line in f:
        print(line.strip())

#create a file named goals.txt
with open("goals.txt", "w") as f:
    f.write("The first goal is to be good in python\n")
    f.write("The second goal is to be good in Gir\n")
    f.write("The third goal is to be good with SQL\n")
    f.write("The fourth goal is to be good in Azure\n")
    f.write("The fifth goal is to be good in AI Engineering")

#read goals.txt and print each goal numbered
with open("goals.txt", "r") as f:
    for i, line in enumerate(f, 1):
        print(f"{i}. {line.strip()}")

def append_to_log(text):
    with open("log.txt", "a") as p:
        p.write(text + "\n")
append_to_log("book")
append_to_log("car")
append_to_log("apple")

with open("log.txt", "r") as p:
    logs = p.read()
    print(logs)


      




