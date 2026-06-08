def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Cannot divide by zero"
result = safe_divide(4, 0)
print(result)

def load_file(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "File not Found"

file_content = load_file("goals.txt")
print(file_content)

while True:
    try:
        num = int(input("Enter a number"))
        print(f"Got it: {num}")
        break
    except ValueError:
        print("Not a number, try again")

def get_valid_number(prompt, minimum, maximum):
    while True:
        try:
            number = int(input(prompt))
            if number >= minimum and number <= maximum:
                return number
                break
            else:
                print(f"Enter a number between {minimum} and {maximum}")
        except ValueError:
            print("Enter a number input")

result = get_valid_number("Pick a number: ", 1, 10)
print(f"You picked = {result}")


 ## the errors file was me trying to understand what error handling was all about  