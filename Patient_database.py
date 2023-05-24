import pandas as pd
import datetime as dt


# data = {'PatientId': list(range(1, 101))*2,
#         'Conditions': [['Fever', 'Cough'], ['Sore throat'], ['Fatigue', 'Headache'], ['Nausea'], ['Chest pain', 'Shortness of breath']] * 20 + 
#                       [['Sore throat', 'Cough'], ['Fever'], ['Chest pain', 'Shortness of breath'], ['Fatigue'], ['Nausea', 'Headache']] * 20,
#         'Date': ['2022-01-01']*101 + ['2022-01-02']*99,
#         }

data1 = [
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
    {'PatientId': 2, 'Conditions': [], 'Date': '2023-05-06'},
]

# create dataframe
df = pd.DataFrame(data1)

df = df.explode('Conditions')

# Convert Date column to datetime type
df['Date'] = pd.to_datetime(df['Date'])

# Add a 'Next_Date' column to store the next date in the group
df['Next_Date'] = df.groupby(['PatientId', 'Conditions'])['Date'].shift(-1)

# Identify the rows where the condition changes (either added or removed)
df['Change'] = (df['Date'] != df['Next_Date'] - pd.Timedelta(days=1))

# Keep only the rows where the condition changes
df = df[df['Change']]

# Drop the 'Change' and 'Next_Date' columns as they are not needed anymore
df = df.drop(['Change', 'Next_Date'], axis=1)

# Create the changelog DataFrame
changelog_df = pd.DataFrame(columns=['PatientId', 'Condition', 'Start_Date', 'End_Date'])

# Iterate through the grouped data to generate the changelog
for _, group in df.groupby(['PatientId', 'Conditions']):
    group = group.reset_index(drop=True)
    for i in range(0, len(group), 2):
        start_date = group.loc[i, 'Date']
        end_date = group.loc[i + 1, 'Date'] if i + 1 < len(group) else "Current"
        changelog_df = changelog_df.append(
            {'PatientId': group.loc[i, 'PatientId'],
             'Condition': group.loc[i, 'Conditions'],
             'Start_Date': start_date,
             'End_Date': end_date},
            ignore_index=True
        )



print(changelog_df)
