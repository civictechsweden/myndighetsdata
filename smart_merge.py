from utils import read_json, write_json, smart_ratio, get_names, get_all_names
from manual_cleaning import clean

SOURCE_NAMES = {
    'esv': 'Ekonomistyrningsverket',
    'stkt': 'Statskontoret',
    'scb': 'SCB',
    'sfs': 'Statens författningssamling',
    'wd': 'Wikidata',
    'agv': 'Arbetsgivarverket',
    'handlingar': 'Handlingar.se'
}

data = {}

for source in SOURCE_NAMES:
    print(f'Loading data from {SOURCE_NAMES[source]}...')
    data[source] = read_json(f'data/{source}.json')

def has_org_nr(source):
    for agency in source:
        if 'org_nr' in source[agency]:
            return True

def get(merged_data, key):
    values = {}
    for source in merged_data:
        data = merged_data[source]
        if key in data:
            values[source] = data[key]

    return values

def find_match(merged_data, key, value):
    for agency in merged_data:
        for source in merged_data[agency]:
            data = merged_data[agency][source]
            if key in data and data[key] == value:
                return agency

    return None

def is_court(org_nr, agency):
    return org_nr == '202100-2742' and agency.lower() != 'domstolsverket'

def merge(data):
    merged_data = {}

    sources = list(data.keys())
    first_source = sources[0]
    other_sources = sources[1:]

    print(f'First source: {SOURCE_NAMES[first_source]}.')
    first_source_data = data[first_source]
    for agency in first_source_data:
        merged_data[agency] = { first_source: first_source_data[agency] }

    for other_source in other_sources:
        print(f'Adding new source: {SOURCE_NAMES[other_source]}')
        other_source_data = data[other_source]

        new_agencies = {}
        all_names = get_all_names(merged_data)

        for agency in other_source_data:
            matched = False
            agency_data = other_source_data[agency]
            org_nr = agency_data['org_nr'] if 'org_nr' in agency_data else None

            if org_nr and not is_court(org_nr, agency):
                match = find_match(merged_data, 'org_nr', org_nr)
                matched = match is not None

            if not matched:
                agency_names = get_names(agency_data)
                agency_names.append(agency)
                match, similarity = smart_ratio(agency_names, all_names)

                # if match is not None and similarity < 99:
                #     print(f'{agency} -> {match} ({similarity})')

            if match is not None:
                if match != agency:
                    if 'other_names' not in agency_data:
                        agency_data['other_names'] = []

                    if agency not in agency_data['other_names']:
                        agency_data['other_names'].append(agency)

                if other_source not in merged_data[match]:
                    merged_data[match][other_source] = agency_data
                else:
                    if isinstance(merged_data[match][other_source], list):
                        merged_data[match][other_source].append(agency_data)
                    else:
                        merged_data[match][other_source] = [
                            merged_data[match][other_source],
                            agency_data
                        ]
            else:
                new_agencies[agency] = { other_source: agency_data }

        for agency in new_agencies:
            merged_data[agency] = new_agencies[agency]

    return merged_data

print('Merging...')
result = merge(data)
print('Merge finished.')
print('Writing to file...')
write_json(result, 'merged')

print('Cleaning...')
clean()
