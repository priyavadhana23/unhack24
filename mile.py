import json


f = open(r'C:\Users\csuser\Desktop\Workshop_Problem\MilestoneInputs\Input\Input\Milestone0.json')
data = json.load(f)

machine_count=0

for i in data['machines']:
    machines='machine_id' # extracting the key value for .....step for id s1 or s2
    no_of_machines=i.get(machines)
    print(f"The value for '{machines}' is: {no_of_machines}")
    if no_of_machines=="M1" and "M2":
        machine_count=2
    step_in_machine='step_id'
    step_in_machine_value=i.get(step_in_machine)
    print(step_in_machine_value)
print(machine_count)

# Iterating through the json list
for i in data['steps']:
    print(i)
    key='id' # extracting the key value for .....step for id s1 or s2
    value=i.get(key)
    print(f"The value for '{key}' is: {value}")
    if type == value: # id is equal to s1
            for i in range(1,3):
                 print()

       


for i in data['machines']:
    print(i)
    machines_count=+1

type = "w1"
S1 =10
S2 =15 
Machines=["M1","M2"]
cooldowntime=5 


for i in data['wafers']:
    key_to_extract = 'type'
    value = data.get(key_to_extract)
    print(f"The value for '{key_to_extract}' is: {value}")
    print(i)
    








# Closing file
f.close()