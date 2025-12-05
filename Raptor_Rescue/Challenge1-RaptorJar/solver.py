import json

with open('logs.json') as file:
    logs = json.load(file)

employee_door_count = {}
habitats = ["1010", "1011", "1012", "2010", "2011", "3010", "3011", "3012", "3013"]

for log in logs:
    emp = log["employee_id"]
    if log["door_id"] in habitats:
        if emp in employee_door_count:
            employee_door_count[emp] += 1
        else:
            employee_door_count[emp] = 1

most_entries = max([[k,v] for k, v in employee_door_count.items()], key=lambda x: x[1])
for k,v in employee_door_count.items():
    if k == most_entries[0]:
        print(k, v, "<- Max")
    else: print(k, v)

print("\nLines in logs where this employee accessed habitats:")
for i, log in enumerate(logs):
    if log["employee_id"] == most_entries[0] and log["door_id"] in habitats:
        print(f"{i}", end=" ")