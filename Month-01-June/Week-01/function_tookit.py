def return_the_larger(a, b):
    if a > b:
        return a
    else:
        return b
larger = return_the_larger(1, 2)
print(larger)

def reverse_the_name(name):
    return name[::-1]
reversed = reverse_the_name("Wonder")
print(reversed)

def item_count(items):
    return len(items)
count = item_count(["apple", "dog", "cat", "spider"])
print(count)

def score_grader(score):
    if score < 0 or score > 100:
        return "Invalid score - enter between 0 and 100"
    elif score >= 70:
        return "A" 
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C" 
    elif score >= 45:
        return "D"
    else:
        return "F"
grade = score_grader(2)
print(grade)