from utils import get, remove_parenthesis

import urllib.request
import pandas as pd

URL = "https://handlingar.se/body/all-authorities.csv"
FILEPATH = 'raw_files/handlingar.csv'

def download():
    urllib.request.urlretrieve(URL, FILEPATH)

def extract():
    agencies = {}

    df = pd.read_csv(FILEPATH)

    for _, row in df.iterrows():
        tags = [
            tag for tag in get(row, "Tags").split(" ") if tag != "not_many_requests"
        ]

        tags_to_take = [
            'forvaltningsmyndighet',
            'riksdagsmyndighet',
            'tingsratt',
            'specialdomstol',
            'forvaltningsratt',
            'hovratt',
            'kammarratt',
            'ambassad'
        ]

        if (any(tag for tag in tags if tag in tags_to_take)
        and 'departement' not in tags):
            name, _ = remove_parenthesis(get(row, 'Name'))
            agencies[name] = {
                'short_name': get(row, 'Short name'),
                'handlingar_url': f'https://handlingar.se/body/{get(row, "URL name")}',
                'tags': tags,
                'website': get(row, 'Home page')
            }

    return agencies
