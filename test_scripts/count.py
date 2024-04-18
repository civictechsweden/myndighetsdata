from utils import read_json

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

merged = read_json('data/merged.json')

for source in SOURCE_NAMES:
    agencies = read_json(f'data/{source}.json')
    count = len(agencies)
    print(f'{SOURCE_NAMES[source]}: {count} agencies, {len([0 for agency in merged if source in merged[agency]])} in merged')
    print([agency for agency in agencies if source not in merged[agency]])

