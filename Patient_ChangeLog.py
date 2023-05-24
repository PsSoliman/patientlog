import pandas as pd
from datetime import datetime

'''
Author: Paul Soliman
Filename: Patient_ChangeLog.py

--------- Overview ----------

Introduction
The ChangeLog class is a Python class that generates a changelog for a given database of patients and their medical conditions. 
The class takes a list of dictionaries as an input, with each dictionary representing a patient entry in the database with associated conditions. 
Each patient entry contains the following keys: PatientId, Conditions, and Date. 
The Conditions key contains a list of medical conditions that the patient has been diagnosed with on the given Date. 
The generate_changelog_df() method of the ChangeLog class generates a pandas DataFrame that represents the changelog of the medical 
conditions for each patient in the database.

Usage
To use the ChangeLog class, you first need to create an instance of the class by passing in the
list of dictionaries representing the patient database as an argument. 
Then, you can call the generate_changelog_df() method to generate the changelog DataFrame.

Bugs
This code may not accurately represent conditions that have had breaks in their occurrence. 
If a condition began on one date, ended on a later date, and then began again at a subsequent time point, 
the code may not correctly reflect this sequence. Instead, the code could suggest that the 
condition has been present continuously since the start date, which could lead to a misunderstanding
of the true condition history.
'''

# Sample data for testing 
data = [
    {'PatientId': 1, 'Conditions': ['Diabetes'], 'Date': '2023-05-01'},
    {'PatientId': 1, 'Conditions': ['Diabetes'], 'Date': '2023-05-02'},
    {'PatientId': 1, 'Conditions': ['Diabetes', 'Hypertension'], 'Date': '2023-05-03'},
    {'PatientId': 1, 'Conditions': ['Diabetes', 'Hypertension'], 'Date': '2023-05-04'},
    {'PatientId': 1, 'Conditions': ['Diabetes'], 'Date': '2023-05-05'},
    {'PatientId': 1, 'Conditions': ['Diabetes'], 'Date': '2023-05-06'},
    {'PatientId': 2, 'Conditions': ['Asthma'], 'Date': '2023-05-01'},
    {'PatientId': 2, 'Conditions': ['Asthma', 'Allergy'], 'Date': '2023-05-02'},
    {'PatientId': 2, 'Conditions': ['Asthma', 'Allergy'], 'Date': '2023-05-03'},
    {'PatientId': 2, 'Conditions': ['Allergy'], 'Date': '2023-05-04'},
    {'PatientId': 2, 'Conditions': ['Allergy'], 'Date': '2023-05-05'},
    {'Conditions': [], 'Date': '2023-05-06', 'PatientId': 2},
]

class ChangeLog():
    '''
    The constructor for the ChangeLog. 
    Given: Database is updated with 1 patient entry per patient per day 
    Assumption: The end date for a patient is the first day they do not report a condtion 

    Fields:
    data - The initial database which the ChangeLog will digest. Should be a list of hashmaps with parameters PatientId, Conditions, and Date
    '''

    # Initializes the ChangeLog
    def __init__(self, data: list):
        self.data = data
        self.changeLog = None
        
    #Populates the ChangeLog
    def generate_changelog_df(self):
        changelog_dict = {}
        
        # Iterates through the given database
        for entry in self.data:
            patient_id = entry['PatientId']
            conditions = entry['Conditions']
            date = datetime.strptime(entry['Date'], '%Y-%m-%d')

            if patient_id not in changelog_dict:
                changelog_dict[patient_id] = {}

            patient_condition = changelog_dict[patient_id]

            for condition in conditions:
                if condition not in patient_condition:
                    patient_condition[condition] = {'start': date, 'end': "Current"}
                else:
                    if patient_condition[condition]['end'] != "Current":
                        patient_condition[condition]['end'] = "Current"

            # Checks for conditions which are no longer current
            for tracked_condition in list(changelog_dict[patient_id].keys()):
                if tracked_condition not in conditions and patient_condition[tracked_condition]['end'] == "Current":
                    patient_condition[tracked_condition]['end'] = date

        # Transforms the nested dictionary into a list of dictionaries
        changelog_list = [
            {'PatientId': patient_id, 'Condition': condition, 'Start Date': info['start'], 'End Date': info['end']}
            for patient_id, conditions in changelog_dict.items()
            for condition, info in conditions.items()
        ]

        # Creates a pandas DF from the list of dictionaries
        self.changelog_df = pd.DataFrame(changelog_list)

        return self.changelog_df


# Printed ChangeLog
test = ChangeLog(data)
test.generate_changelog_df()
print(test.changelog_df)