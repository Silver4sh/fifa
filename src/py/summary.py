import pandas as pd
import csv

data = pd.read_csv(path_import).drop('Unnamed: 0', axis=1)

## Processing
club_data = []
for club in data.Club.unique():
    count_ = data.loc[data['Club'] == club, 'Name'].count()
    att = round(data.loc[
        (data['Club'] == club) & (data['Position'].isin(['CF', 'SS', 'LW', 'RW', 'ST', 'FW'])),
        'Overall'
    ].mean(), 2)
    mid = round(data.loc[
        (data['Club'] == club) & (data['Position'].str.contains('M', na=False)),
        'Overall'
    ].mean(), 2)
    deff = round(data.loc[
        (data['Club'] == club) & ((data['Position'].str.contains('B', na=False)) | (data['Position'] == 'SW')),
        'Overall'
    ].mean(), 2)
    average = round(data.loc[data['Club'] == club, 'Overall'].mean(), 2)
    
    club_data.append([club, count_, att, mid, deff, average])

nation_data = []
for nation in data.Nation.unique():
    count_ = data.loc[data['Nation'] == nation, 'Name'].count()
    nation_avg = round(data.loc[data['Nation'] == nation, 'Overall'].mean(), 2)
    nation_data.append([nation, count_, nation_avg])

position_count = []
for pos in data.Position.unique():
    count_ = data.loc[data['Position'] == pos, 'Name'].count()
    position_count.append([pos, count_])

club_data = sorted(club_data, key=lambda x: x[4], reverse=True)

with open(path_eksport, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Club', 'Player', 'ATTK', 'MID', 'DEFF', 'Overall'])
    for row in club_data:
        writer.writerow(row)