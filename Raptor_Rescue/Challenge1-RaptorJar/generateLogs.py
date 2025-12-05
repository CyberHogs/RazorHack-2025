import json
import random
import uuid
from datetime import datetime, timedelta

employees = {
    "10C967" : "Dr. Chris Rootkit",
    "10C96F" : "Pterry Dactyl",
    "10C96A" : "Sarah Tops",
    "10C972" : "Iguana Donna",
    "10C974" : "Barry Onyx",
    "10C975" : "Ellie Saddler",
    "10C970" : "Maxwell Brooks",
    "10C96E" : "Herb Avour",
    "10C96B" : "Tyr Rex",
    "10C96C" : "Leo Raptorri",
    "10C971" : "Chef J. Pex",
    "10C973" : "Ali Gator",
    "10C96D" : "Kronk",
    # "10C966" : "Evan Soris",
    # "" : "Barbara Saul",
    "10F092" : "Dino Research Intern"
}

chef = ""
intern = ""
for i_d, name in employees.items():
    if "Chef" in name:
        chef = i_d
    if "Intern" in name:
        intern = i_d

doors = {
    "Main Hallway": {
        "Main Gate" : "0000",
        "Electrical": "0100",
        "Veterinary Clinic": "0101",
        "Office": "0102",
        "Enclosure A": {
            "Main Gate": "1000",
            "Maintenance Closet": "1100",
            "Storage": "1101",
            "Habitat A": "1010",
            "Habitat B": "1011",
            "Habitat C": "1012"
        },
        "Enclosure B": {
            "Main Gate": "2000",
            "Maintenance Closet": "2100",
            "Storage": "2101",
            "Habitat A": "2010",
            "Habitat B": "2011"
        },
        "Enclosure C": {
            "Main Gate": "3000",
            "Maintenance Closet": "3100",
            "Storage": "3101",
            "Habitat A": "3010",
            "Habitat B": "3011",
            "Habitat C": "3012",
            "Habitat D": "3013"
        }
    }
}

# Example Log Entry
# {
#   "event_id":"b9f1c0a6-3d2e-4f6d-8a3a-2b7d9e1f4c0a",
#   "timestamp":"2025-10-12T21:42:03",
#   "employee_id":"<binary_num>",
#   "door_id":"<id>",
#   "reader_type":"prox",
#   "direction":"<enter or exit>",
# }

#                             Employees with habitat access
#              Pterry Dactyl Iguana Don Herb Avour Leo Rapt. Ali Gator
habitat_allowed = {"10C96F", "10C972", "10C96E", "10C96C", "10C973"}

start_timeframe = datetime(2025, 11, 3)
end_timeframe = datetime(2025, 11, 7)
days = [i for i in range(start_timeframe.day, end_timeframe.day + 1)]

# Door map reading
def flatten_doors(tree, parent_path=None, parent_doors=None):
    """
    Returns mapping of full paths to its path of door IDs
    e.g. "Main Hallway/Electrical" -> ["0000", "0100"]
    """
    flat = {}
    for name, val in tree.items():
        path = f"{parent_path}/{name}" if parent_path else name
        if isinstance(val, dict):
            next_door = next(iter(val.values()))
            flat.update(flatten_doors(val, path, parent_doors + [next_door] if parent_doors else [next_door]))
        else:
            doors = parent_doors
            if name != "Main Gate":
                doors = doors + [val] if doors else [val]
            flat[path] = doors
    return flat

# All possible destinations for employees
paths = flatten_doors(doors)
main_entrance = next(iter(paths))
max_path_length = max([len(p) for p in paths.values()])

# Time functions
def random_timestamp(day):
    return datetime(2025, 11, day, 0, 0, 0) + timedelta(hours=random.randint(0,23), minutes=random.randint(0,59), seconds=random.randint(0,59))

def rand_increment_date(time, start=0, end=30):
    return time + timedelta(seconds=random.randint(start, end))

# Log generator
def generate_event(emp_id, door_id, direction, timestamp):
    return {
        "event_id": str(uuid.uuid4()),
        "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
        "employee_id": emp_id,
        "door_id": door_id,
        "reader_type": "prox",
        "direction": direction
    }

# Simulation functions
def get_accessible_paths(emp_id):
    """Return list of leaf door paths the employee may access (filter habitats if necessary)."""
    if emp_id in habitat_allowed:
        return paths
    else:
        return {p:ids for p, ids in paths.items() if "Habitat" not in p}

def simulate_employee_journey(emp_id, day, action_budget=8, enter_chance=0.7):
    """
    Simulate a sequence of valid enter/exit actions for a single employee.
    - Ensures prerequisites are entered before deeper doors.
    - Exits happen in correct order
    - Will not enter room just exited or leave immediately after entering main entrance
    - action_budget is approximate number of enters/exits (once budget exhausted, it will exit remaining rooms if any).
    """
    logs = []
    current_rooms = []   # stack of entered doors
    accessible = get_accessible_paths(emp_id)
    start_time = random_timestamp(day)
    current_time = start_time
    entered = False
    last_room = ""

    for _ in range(action_budget):
        # Determine candidate doors to enter:
        valid_paths = {
            "enter": [],
            "exit": []
        }
        if len(current_rooms) == 0:
            if entered: return logs
            current_rooms = accessible[main_entrance].copy()
            logs.append(generate_event(emp_id, current_rooms[-1], "enter", current_time))
            current_time = rand_increment_date(current_time)
            entered = True
            continue
        else:
            for path_ids in accessible.values():
                if len(current_rooms) != max_path_length and len(path_ids) == len(current_rooms) + 1 and path_ids[-2][0] == current_rooms[-1][0]:
                    valid_paths["enter"].append(path_ids.copy())
                if len(path_ids) == len(current_rooms) - 1 and path_ids[-1][0] == current_rooms[-2][0]:
                    valid_paths["exit"].append(path_ids.copy())

        # 60% chance to attempt entering if candidates exist; otherwise try to exit if possible
        if valid_paths["enter"] and (random.random() < enter_chance or not valid_paths["exit"]):
            # choose a door to go into
            while True:
                current_rooms = random.choice(valid_paths["enter"])
                if current_rooms[-1] != last_room:
                    last_room = current_rooms[-1]
                    break
            logs.append(generate_event(emp_id, current_rooms[-1], "enter", current_time))
            current_time = rand_increment_date(current_time)
        elif valid_paths["exit"]:
            # Attempt to exit
            last_room = current_rooms.pop()
            logs.append(generate_event(emp_id, last_room, "exit", current_time))
            current_time = rand_increment_date(current_time)
        else:
            print("Error: no valid path to take")

    while current_rooms:
        last = current_rooms.pop()
        logs.append(generate_event(emp_id, last, "exit", current_time))
        current_time = rand_increment_date(current_time)

    # print("Done with", emp_id)
    # print(action_budget, "actions:")
    # for log in logs:
    #     print(log)
    return logs


# Chef J Pex anomaly injection
def generate_anomaly(start_time):
    """
    Append suspicious sequences:
    - Chef (10C971) enters an enclosure main gate.
    - Shortly afterwards the intern (10F092) is logged entering/exiting a habitat WITHOUT preceding door prereqs.
    """
    chef_time = start_time
    gate_paths = []
    habitat_paths = []
    for path, doors in paths.items():
        if "Enclosure" in path:
            if len(doors) == 2:
                gate_paths.append(doors)
            if "Habitat" in path:
                habitat_paths.append(doors)
    
    logs = []

    chosen_gate = random.choice(gate_paths)
    for door in chosen_gate:
        logs.append(generate_event(chef, door, "enter", chef_time))
        chef_time = chef_time + timedelta(seconds=random.randint(5,15))

    # intern enters a habitat soon after (skip prereq doors)
    habitat_id = random.choice([path for path in habitat_paths if path[1] == chosen_gate[1]])[-1]
    logs.append(generate_event(intern, habitat_id, "enter", chef_time))
    chef_time = chef_time + timedelta(seconds=random.randint(30, 300))

    logs.append(generate_event(intern, habitat_id, "exit", chef_time))
    chef_time = chef_time + timedelta(seconds=random.randint(5,15))

    for door in reversed(chosen_gate):
        logs.append(generate_event(chef, door, "exit", chef_time))
        chef_time = chef_time + timedelta(seconds=random.randint(5,15))

    return chef_time, logs

# Main Log Generator
def generate_logs(min_actions, max_actions, seed=0, output_file="logs.json"):
    """
    - min_actions: lower bound of random action budget (must be even)
    - max_actions: upper bound of random action budget (must be even)
    - chef_extra: number of Chef+Intern suspicious sequences to append (chef_extra*2 entries added to logs)
    - seed: random seed to use for generation
    - output_file: name of log output file
    """

    logs = []
    if (min_actions % 2 != 0 or max_actions % 2 != 0):
            assert ValueError("Must have even min_actions and max_actions")
    
    random.seed(seed)
    diff = max_actions - min_actions

    for day in days:
        for emp in employees:
            if emp != chef and emp != intern: logs.extend(simulate_employee_journey(emp, day, action_budget=min_actions + 2*random.randint(0, diff//2)))
        first_time = random_timestamp(day)
        second_time = first_time

        end_time, new_logs = generate_anomaly(first_time)
        logs.extend(new_logs)

        while first_time - timedelta(hours=3) <= second_time <= end_time + timedelta(hours=3):
            second_time = random_timestamp(day)

        end_time, new_logs = generate_anomaly(second_time)
        logs.extend(new_logs)


    # sort chronologically
    logs.sort(key=lambda e: e["timestamp"])

    # write JSON
    with open(output_file, "w", encoding="utf-8") as fh:
        json.dump(logs, fh, indent=2)

    print(f"Generated {len(logs)} events -> {output_file}")

if __name__ == "__main__":
    generate_logs(min_actions=4, max_actions=10, seed=5)
