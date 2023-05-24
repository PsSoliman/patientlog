from datetime import datetime, date, timedelta
from Patient_ChangeLog import ChangeLog 
import random
import pandas as pd
pd.set_option('display.max_rows', None)


def test_no_data():
    '''
    Tests an empty database
    '''

    data = []
    expected_output = []
    changelog = ChangeLog(data)


def test_single_patient_single_condition():
    '''
    Tests that a single patient will have a given condition reflected in the output
    '''

    data = [{'PatientId': 1,
     'Conditions': ['Fever'], 'Date': '2022-01-01'}]
    expected_output = [{'PatientId': 1, 'Condition': 'Fever', 'Start Date': datetime(2022, 1, 1), 'End Date': 'Current'}]
    changelog = ChangeLog(data)
    changelog.generate_changelog_df()
    assert changelog.changelog_df.to_dict('records') == expected_output


def test_single_patient_multiple_conditions():
    '''
    Tests that a single patient with multiple conditions will be initialized correctly in the change log
    '''

    data = [{'PatientId': 1, 'Conditions': ['Fever', 'Headache', 'Cough'], 'Date': '2022-01-01'}]
    expected_output = [
        {'PatientId': 1, 'Condition': 'Fever', 'Start Date': datetime(2022, 1, 1), 'End Date': 'Current'},
        {'PatientId': 1, 'Condition': 'Headache', 'Start Date': datetime(2022, 1, 1), 'End Date': 'Current'},
        {'PatientId': 1, 'Condition': 'Cough', 'Start Date': datetime(2022, 1, 1), 'End Date': 'Current'}
    ]
    changelog = ChangeLog(data)
    changelog.generate_changelog_df()
    assert changelog.changelog_df.to_dict('records') == expected_output



def test_generate_changelog_df():
    '''
    Tests that multiple patient databases are initialized correctly in the change log
    '''

    data = [
        {'PatientId': 1, 'Conditions': ['Diabetes'], 'Date': '2023-05-01'},
        {'PatientId': 1, 'Conditions': ['Diabetes'], 'Date': '2023-05-02'},
        {'PatientId': 1, 'Conditions': ['Diabetes', 'Hypertension'], 'Date': '2023-05-03'},
        {'PatientId': 1, 'Conditions': ['Diabetes', 'Hypertension'], 'Date': '2023-05-04'},
        {'PatientId': 1, 'Conditions': ['Diabetes'], 'Date': '2023-05-05'},
        {'PatientId': 1, 'Conditions': ['Hypertension'], 'Date': '2023-05-06'},
        {'PatientId': 2, 'Conditions': ['Asthma'], 'Date': '2023-05-01'},
        {'PatientId': 2, 'Conditions': ['Asthma', 'Allergy'], 'Date': '2023-05-02'},
        {'PatientId': 2, 'Conditions': ['Asthma', 'Allergy'], 'Date': '2023-05-03'},
        {'PatientId': 2, 'Conditions': ['Allergy'], 'Date': '2023-05-04'},
        {'PatientId': 2, 'Conditions': [], 'Date': '2023-05-05'},
        {'PatientId': 2, 'Conditions': [], 'Date': '2023-05-06'},
    ]

    changelog = ChangeLog(data)
    df = changelog.generate_changelog_df()

    assert len(df) == 4
    assert df[df['Condition'] == 'Diabetes']['Start Date'].iloc[0] == datetime(2023, 5, 1)
    assert df[df['Condition'] == 'Diabetes']['End Date'].iloc[0] == datetime(2023, 5, 6)
    assert df[df['Condition'] == 'Hypertension']['Start Date'].iloc[0] == datetime(2023, 5, 3)
    assert df[df['Condition'] == 'Hypertension']['End Date'].iloc[0] == "Current"
    assert df[df['Condition'] == 'Asthma']['End Date'].iloc[0] == datetime(2023, 5, 4)
    assert df[df['Condition'] == 'Allergy']['End Date'].iloc[0] == datetime(2023, 5, 5)




def test_multiple_patients_multiple_conditions():
    '''
    Tests that disorganized patientId databases still initialize the change log correctly
    '''

    data = [
        {'PatientId': 1, 'Conditions': ['Fever'], 'Date': '2022-01-01'},
        {'PatientId': 2, 'Conditions': ['Headache'], 'Date': '2022-01-01'},
        {'PatientId': 2, 'Conditions': ['Headache'], 'Date': '2022-01-02'},
        {'PatientId': 1, 'Conditions': ['Cough'], 'Date': '2022-01-02'},
        {'PatientId': 1, 'Conditions': [], 'Date': '2022-01-03'},
        {'PatientId': 2, 'Conditions': ['Fever'], 'Date': '2022-01-03'},
        {'PatientId': 2, 'Conditions': ['Fever'], 'Date': '2022-01-04'},
        {'PatientId': 1, 'Conditions': [], 'Date': '2022-01-04'}
    ]
    expected_output = [
        {'PatientId': 1, 'Condition': 'Fever', 'Start Date': datetime(2022, 1, 1), 'End Date': datetime(2022, 1, 2)},
        {'PatientId': 1, 'Condition': 'Cough', 'Start Date': datetime(2022, 1, 2), 'End Date': datetime(2022, 1, 3)},
        {'PatientId': 2, 'Condition': 'Headache', 'Start Date': datetime(2022, 1, 1), 'End Date': datetime(2022, 1, 3)},
        {'PatientId': 2, 'Condition': 'Fever', 'Start Date': datetime(2022, 1, 3), 'End Date': 'Current'}
    ]
    changelog = ChangeLog(data)
    changelog.generate_changelog_df()
    assert changelog.changelog_df.to_dict('records') == expected_output


# This function randomly generates a database for 100 patients on 100 consecutive days
def database_Generator(start_date, num_days):

    data = []
    for patient_id in range(0, 100):

        conditions = ['Diabetes', 'Hypertension', 'Asthma', 'Allergy']
        num_conditions = random.randint(0, 2)
        patient_data = []

        for i in range(num_days):
            entry_date = start_date + timedelta(days=i)
            if i == 0:
                entry_conditions = random.sample(conditions, num_conditions)
            else:
                last_entry = patient_data[-1]
                if last_entry['Conditions'] == []:
                    entry_conditions = random.sample(conditions, num_conditions)
                else:
                    entry_conditions = last_entry['Conditions']
                    entry_conditions = random.sample(conditions, num_conditions)
            patient_data.append({'PatientId': patient_id, 'Conditions': entry_conditions, 'Date': str(entry_date)})
        data.extend(patient_data)
    return data


def test_length():
    '''
    Tests that the changelog initializes large databases correctly
    '''

    data = database_Generator(date(2023, 5, 1), 100)

    test = ChangeLog(data)
    test.generate_changelog_df()
    print(test.changelog_df)

