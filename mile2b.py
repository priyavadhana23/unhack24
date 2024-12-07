import json

f = open(r'C:\Users\csuser\Desktop\Workshop_Problem\MilestoneInputs\Input\Input\Milestone3a.json')
data = json.load(f)

machine_states = {}


for machine in data['machines']:
    machine_states[machine['machine_id']] = {
        'step_id': machine['step_id'],
        'cooldown_time': machine['cooldown_time'],
        'parameters': machine['initial_parameters'].copy(),
        'fluctuation': machine['fluctuation'],
        'processed_wafers': 0,
        'next_available_time': 0,
        'n': machine['n'],  
    }

schedule = []

def is_within_range(machine, step):
    for param, value in machine['parameters'].items():
        min_val, max_val = step['parameters'][param]
        if not (min_val <= value <= max_val):
            return False
    return True

def process_wafer(wafer_id, step_id, machine_id, start_time, processing_time):
    machine = machine_states[machine_id]
    
    machine['processed_wafers'] += 1
    for param in machine['parameters']:
        machine['parameters'][param] += machine['fluctuation'][param]  
    
    schedule.append({
        'wafer_id': wafer_id,
        'step': step_id,
        'machine': machine_id,
        'start_time': start_time,
        'end_time': start_time + processing_time
    })
    
    
    if machine['processed_wafers'] >= machine['n']:
        if 'initial_parameters' in machine:
            machine['parameters'] = machine['initial_parameters'].copy()  
        else:
            machine['parameters'] = {param: 100 for param in machine['parameters']}  
        machine['next_available_time'] = start_time + processing_time + machine['cooldown_time']
        machine['processed_wafers'] = 0  
    else:
        machine['next_available_time'] = start_time + processing_time


current_time = 0


for wafer in data['wafers']:
    wafer_type = wafer['type']
    quantity = wafer['quantity']
    processing_times = wafer['processing_times']
    

    for i in range(quantity):
        wafer_id = f"{wafer_type}-{i+1}"

   
        for step_id, processing_time in processing_times.items():
            step = next(s for s in data['steps'] if s['id'] == step_id)

 
            while True:
                available_machines = [
                    machine_id for machine_id, machine in machine_states.items()
                    if machine['step_id'] == step_id and machine['next_available_time'] <= current_time
                ]
                
                if available_machines:
                    for machine_id in available_machines:
                        if is_within_range(machine_states[machine_id], step):
                            process_wafer(wafer_id, step_id, machine_id, current_time, processing_time)
                            current_time += processing_time  
                            break
                    break  
                else:
                    current_time += 1  
                    continue

output_path = r'final_schedule3a.json'
with open(output_path, 'w') as outfile:
   
    json.dump({"schedule": schedule}, outfile, separators=(',', ':'), indent=1)

print(f"Schedule has been saved to {output_path}")