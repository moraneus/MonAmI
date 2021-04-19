import string
import random
import json

def atom_generator(size=10, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def create_file(size=30):
    intervals = []
    for i in range(size):
        name = atom_generator()
        start = random.randint(0, 500000)
        intervals.append([name, 'begin', start])
        intervals.append([name, 'end', random.randint(start, 500000)])
    intervals.sort(key=lambda x: x[2])
    execution = []

    for interval in intervals:
        if interval[1] == 'begin':
            execution.append([interval[1], interval[0], f"data_{interval[2]}"])
        else:
            execution.append([interval[1], interval[0]])

    with open('input', 'r') as file:
        data = json.load(file)

    data["execution"] = execution

    with open('input', 'w') as file:
        json.dump(data, file)

create_file()
