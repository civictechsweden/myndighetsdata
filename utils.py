import re
import json
from rapidfuzz import fuzz

def remove_parenthesis(name):
    match = re.search(r'(.+) ?\(([a-zA-Z]{2,10})\)', name)

    if match and len(match.groups()) == 2:
        return [name.strip() for name in match.groups()]
    else:
        return name, None

def get(row, label):
        if label not in row.keys():
            return ''

        value = row.loc[label]
        value = value if not value != value else ''
        if isinstance(value, str):
            value = value.strip()
        elif isinstance(value, float) and value.is_integer():
            value = int(value)
        return value

def read_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json(data, name):
    with open(f'{name}.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def smart_ratio(names, choices, threshold = 90):
    smart_ratio = 0
    best_match = None

    for name in names:
        for choice in choices:
            name_cleaned = name.lower()
            choice_cleaned = choice.lower()

            to_remove = [
                'förvaltningsrätten',
                'lokala',
                'arrendenämnd',
                'tingsrätt',
                'hovrätt',
                'domstol',
                'sverige',
                'svensk',
                'ambassad',
                'konsulat',
                'arkivet',
                'regionala',
                'staten',
                'institut',
                'styrelse',
                'universitet',
                'högskol',
                'länsstyrelse',
                'universitet',
                'avvecklingsmyndigheten för',
                'myndighet',
                'verk'
            ]

            for word in to_remove:
                if word in name_cleaned and word in choice_cleaned:
                    name_cleaned = name_cleaned.replace(word, '')
                    choice_cleaned = choice_cleaned.replace(word, '')

            to_remove_unilateral = [
                ' och arrende',
                ' o mark o miljö och patent',
                ' och mark och miljödomstol',
                ' och migrationsdomstol',
                ' och migrationsöverdomst',
                ' och migrationsdom',
                ' kärntekniska anläggningen',
                ' och patent och marknadsdom',
                'älhavaren'
            ]

            for word in to_remove_unilateral:
                name_cleaned = name_cleaned.replace(word, '')
                choice_cleaned = choice_cleaned.replace(word, '')

            ratio = fuzz.ratio(name_cleaned, choice_cleaned)

            if ratio > smart_ratio:
                smart_ratio = ratio
                best_match = choice

        similarity = smart_ratio if len(name) >= 4 and len(best_match) >= 4 else 0

    if similarity >= threshold:
        return choices[best_match], similarity
    else:
        return None, similarity

def get_sfs(text):
    if not text:
        return None

    match = re.search(r'\d{4}:\d{1,4}', text)

    if match:
        return match[0]

def get_names(data, include_alt = True, include_old = True):
    agency_names = []

    if include_alt and 'name_en' in data:
        agency_names.append(data['name_en'])

    if include_alt and 'short_name' in data:
        agency_names.append(data['short_name'])

    if include_old and 'old_names' in data:
        agency_names.extend(data['old_names'])

    if 'other_names' in data:
        agency_names.extend(data['other_names'])

    return agency_names

def get_all_names(merged_data, include_alt = True, include_old = False):
    all_names = {}

    for main_name in merged_data:
        for source in merged_data[main_name]:
            data = merged_data[main_name][source]

            agency_names = [main_name]
            agency_names.extend(get_names(data, include_alt))

            for name in agency_names:
                if len(name) >= 4:
                    all_names[name] = main_name

    return all_names


