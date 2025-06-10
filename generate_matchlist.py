import json
import pandas as pd

with open('data/merged.json', 'r', encoding='utf-8') as file:
    merged = json.load(file)

agency_names = []

def add(name, official_name):
    if name and official_name:
        agency_names.append({
            'name': name.lower(),
            'official_name': official_name
        })

for name in merged:
    data = merged[name]
    add(name, name)

    for source in data:
        source_data = data[source]

        if isinstance(source_data, dict):
            source_data = [source_data]
        
        for item in source_data:
            add(item.get('name_en'), name)
            add(item.get('short_name'), name)

            old_names = item['old_names'] if item.get('old_names') else []
            other_names = item['other_names'] if item.get('other_names') else []
        
            for other_name in old_names + other_names:
                add(other_name, name)

pd.DataFrame(agency_names).drop_duplicates().to_csv('data/matchlist.csv', index=False)