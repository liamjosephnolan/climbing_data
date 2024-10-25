import yaml
from datetime import datetime
from bs4 import BeautifulSoup
class ClimbingSession:
    def __init__(self, weight, day_on, start_time, date):
        self.weight = weight  # in kilograms
        self.date = date       # date
        self.day_on = day_on   # number of climbing days
        self.start_time = start_time  # start time as a string

class Kilter(ClimbingSession):
    def __init__(self, weight, day_on, start_time, date, angle, V6, V7, V8, V9, V10, V11, V12, V13):
        super().__init__(weight, day_on, start_time, date)  # Correct call to parent class
        self.angle = angle
        self.V6 = V6
        self.V7 = V7
        self.V8 = V8
        self.V9 = V9
        self.V10 = V10
        self.V11 = V11
        self.V12 = V12
        self.V13 = V13

# Specify the path to your markdown file
file_path = "10_17_2024_training_updated.md"

# Open the file in read mode
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

yaml_part = content.split('---')[1].strip()

try:
    config = yaml.safe_load(yaml_part)
    
    # Access the parameters
    date = config.get('date')
    start_time = config.get('start_time')
    weight = config.get('weight')  
    day_on = config.get('day_on')

    print(f"Weight: {weight}")
    print(f"Date: {date}")
    print(f"Start Time: {start_time}")
    print(f"Day On: {day_on}")
    
except Exception as e:
    print(f"Error parsing YAML: {e}")

# Create an instance of ClimbingSession
climbing_session = ClimbingSession(weight=weight, day_on=day_on, start_time=start_time, date=date)

# Now create an instance of Kilter
kilter = Kilter(
    weight=weight,      # Provide weight
    day_on=day_on,     # Provide days on
    start_time=start_time,  # Provide start time
    date=date,          # Provide date
    angle=45,          # Example angle
    V6=5.10,           # Example V6 value
    V7=5.11,           # Example V7 value
    V8=4,              # Set V8 to 4
    V9=5.12,           # Example V9 value
    V10=5.13,          # Example V10 value
    V11=5.14,          # Example V11 value
    V12=5.15,          # Example V12 value
    V13=5.16           # Example V13 value
)


# Find the positions of the headers
kilter_start = content.find("# **Kilter**")
hangboard_start = content.find("#  **Hangboard**")

# Extract the content between the two headers
if kilter_start != -1 and hangboard_start != -1:
    html_content = content[kilter_start:hangboard_start].strip()
else:
    print("One of the headers was not found in the content.")


kilter_soup = BeautifulSoup(html_content,'html.parser')


# Find all input elements that have the 'checked' attribute
checked_elements = kilter_soup.find_all(lambda tag: tag.name == "input" and tag.has_attr('checked'))

# Extract and print the ids of the checked elements
checked_ids = [element.get('id') for element in checked_elements]
print(checked_ids)


# Filter out angle IDs (those that start with 'angle_')
angle_ids = [id for id in checked_ids if id.startswith('angle_')]

if len(angle_ids) > 1:
    print("Too many angles set")
else:
    kilter.angle = angle_ids[0].split('_')[1]


print(f"The angle is: {kilter.angle}")

