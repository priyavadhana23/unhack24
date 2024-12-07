import json


f = open(r'C:\Users\csuser\Desktop\Workshop_Problem\MilestoneInputs\Input\Input\Milestone0.json')
data = json.load(f)

# Initialize machine states
machine_states = {}
for machine in data['machines']:
    machine_states[machine['machine_id']] = {
        'step_id': machine['step_id'],
        'cooldown_time': machine['cooldown_time'],
        'parameters': machine['initial_parameters'].copy(),
        'fluctuation': machine['fluctuation'],
        'processed_wafers': 0,
        'next_available_time': 0,
        'n': machine['n'],  # Number of wafers before cooldown
    }

# Store the schedule of when each wafer is processed
schedule = []

# Function to check if machine's parameters are within the allowed range
def is_within_range(machine, step):
    for param, value in machine['parameters'].items():
        min_val, max_val = step['parameters'][param]
        if not (min_val <= value <= max_val):
            return False
    return True

# Function to process a wafer on a machine
def process_wafer(wafer_id, step_id, machine_id, start_time, processing_time):
    machine = machine_states[machine_id]
    
    # Update machine's processed wafer count and parameters
    machine['processed_wafers'] += 1
    for param in machine['parameters']:
        machine['parameters'][param] += machine['fluctuation'][param]  # Adjust parameters based on fluctuation
    
    # Add the processing details to the schedule
    schedule.append({
        'wafer_id': wafer_id,
        'step': step_id,  # Changed from 'step_id' to 'step'
        'machine': machine_id,  # Changed from 'machine_id' to 'machine'
        'start_time': start_time,
        'end_time': start_time + processing_time
    })
    
    # If the machine has processed enough wafers, reset parameters and set cooldown
    if machine['processed_wafers'] >= machine['n']:
        machine['parameters'] = machine['fluctuation']['initial_parameters'].copy()  # Reset to initial
        machine['next_available_time'] = start_time + processing_time + machine['cooldown_time']
        machine['processed_wafers'] = 0  # Reset wafer count
    else:
        machine['next_available_time'] = start_time + processing_time

# Main scheduling loop
current_time = 0
for wafer in data['wafers']:
    wafer_type = wafer['type']
    quantity = wafer['quantity']
    processing_times = wafer['processing_times']
    
    # Process each wafer
    for i in range(quantity):
        wafer_id = f"{wafer_type}-{i+1}"

        # Process each step for the wafer (e.g., S1, S2)
        for step_id, processing_time in processing_times.items():
            step = next(s for s in data['steps'] if s['id'] == step_id)

            # Find all available machines for the current step
            while True:
                available_machines = [
                    machine_id for machine_id, machine in machine_states.items()
                    if machine['step_id'] == step_id and machine['next_available_time'] <= current_time
                ]
                
                # Process the wafer on an available machine
                if available_machines:
                    for machine_id in available_machines:
                        if is_within_range(machine_states[machine_id], step):
                            process_wafer(wafer_id, step_id, machine_id, current_time, processing_time)
                            current_time += processing_time  # Update the current time
                            break
                    break  # Move to the next wafer after a machine is selected
                else:
                    current_time += 1  # If no machine is available, move time forward
                    continue


output_path = r'final_schedule.json'
with open(output_path, 'w') as outfile:
   
    json.dump({"schedule": schedule}, outfile, separators=(',', ':'), indent=1)

print(f"Schedule has been saved to {output_path}")
