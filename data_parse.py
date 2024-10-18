import yaml

class ClimbingSession:
    def __init__(self, weight, days_on, start_time):
        self.weight = weight  # in kilograms
        self.days_on = days_on  # number of climbing days
        self.start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")  # start 15:18

# Specify the path to your markdown file
file_path = "10_17_2024_training.md"

# Open the file in read mode
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

yaml_part =content.split('---')[1].strip()


try:
    config = yaml.safe_load(yaml_part)
    
    # Access the weight parameter
    weight = config.get('weight')  # No need for nested get here since 'weight' is at the top level
    print(f"Weight: {weight}")
    
except Exception as e:
    print(f"Error parsing YAML: {e}")
   
