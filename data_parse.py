import yaml
import pandas as pd
import os
from datetime import datetime
from bs4 import BeautifulSoup
   

# Class Definitons
class ClimbingSession:
    def __init__(self, weight, day_on, start_time, date):
        self.weight = weight  # in kilograms
        self.date = date       # date
        self.day_on = day_on   # number of climbing days
        self.start_time = start_time  # start time as a string

class Kilter(ClimbingSession):
    def __init__(self, weight, day_on, start_time, date, angle=None, V6=None, V7=None, V8=None, V9=None, V10=None, V11=None, V12=None, V13=None):
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

# Fucntion to parse file and extract relevant parameters
def file_parse(file_path):

    # Open the file in read mode
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    yaml_part = content.split('---')[1].strip() # Split the YAML part

    try:
        config = yaml.safe_load(yaml_part)
        
        # Access the parameters
        date = config.get('date')
        start_time = config.get('start_time')
        weight = config.get('weight')  
        day_on = config.get('day_on')

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
    )

    # Find the positions of the headers
    kilter_start = content.find("# **Kilter**")
    hangboard_start = content.find("#  **Hangboard**")

    # Extract the content between the two headers
    if kilter_start != -1 and hangboard_start != -1:
        kilter_content = content[kilter_start:hangboard_start].strip()
    else:
        print("One of the headers was not found in the content.")

    kilter_soup = BeautifulSoup(kilter_content,'html.parser')

    # Find all input elements that have the 'checked' attribute
    checked_elements = kilter_soup.find_all(lambda tag: tag.name == "input" and tag.has_attr('checked'))

    # Extract and print the ids of the checked elements
    checked_ids = [element.get('id') for element in checked_elements]

    # Filter out angle IDs (those that start with 'angle_')
    angle_ids = [id for id in checked_ids if id.startswith('angle_')]

    if len(angle_ids) > 1:
        print("Too many angles set")
    else:
        kilter.angle = angle_ids[0].split('_')[1]

    # parse for grade id's, split them and convert into int 
    grade_ids = list(map(int,[id.split('V')[1].split('-')[0] for id in checked_ids if id.startswith('grade_')]))

    grade_ids = pd.Series(grade_ids).value_counts()

    kilter.V6 = grade_ids.get(6,0)
    kilter.V7 = grade_ids.get(7,0)
    kilter.V8 = grade_ids.get(8,0)
    kilter.V9 = grade_ids.get(9,0)
    kilter.V10 = grade_ids.get(10,0)
    kilter.V11 = grade_ids.get(11,0)
    kilter.V12 = grade_ids.get(12, 0)
    kilter.V13 = grade_ids.get(13,0)
    kilter.V14 = grade_ids.get(14,0)
    
    climbing_session.kilter = kilter # Attach kilter to climbing_session class
    return climbing_session

folder_path = "./training_data/"
all_data = []
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    climbing_session = file_parse(file_path)
    all_data.append((filename, climbing_session))

second_day_v8_grade = all_data[2][1]
second_day_v8_grade = second_day_v8_grade.kilter.V8

print(second_day_v8_grade)
