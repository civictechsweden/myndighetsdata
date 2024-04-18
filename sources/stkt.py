from utils import get, get_sfs

from bs4 import BeautifulSoup
import requests
import pandas as pd

DOMAIN = 'https://www.statskontoret.se'
PAGE_URL = '/fokusomraden/fakta-om-statsforvaltningen/myndigheterna-under-regeringen'
FILEPATH = 'raw_files/stkt.xlsx'

def download():
    r = requests.get(DOMAIN + PAGE_URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    link = soup.find('a', text=lambda t: t and 'Öppna data' in t)
    r = requests.get(DOMAIN + link['href'])
    with open(FILEPATH, 'wb') as outfile:
        outfile.write(r.content)

def extract():
    agencies = {}

    df = pd.read_excel(FILEPATH, 'Myndighetsregister')

    fte_columns = [column for column in df.columns
                   if 'ÅA_2' in column or 'ÅA 2' in column]

    for _, row in df.iterrows():

        name = get(row, 'Myndighet')

        if any(name == word for word in ['', 'Totalt', 'Övriga']):
            continue
        elif name == 'Kommentarer':
            break

        created_by = get_sfs(str(get(row, 'SFS')))
        latest_updated_by = get_sfs(get(row, 'Senaste SFS'))

        stkt_data = {
                        'department': get(row, 'Departement'),
                        'org_nr': get(row, 'Orgnr'),
                        'cofog': get(row, 'COFOG'),
                        'cofog10': get(row, 'COFOG10'),
                        'host': get(row, 'Värdmyndighet'),
                        'structure': get(row, 'Ledningsform'),
                        'has_gd': str(get(row, 'GD')) == '1',
                        'created_by': created_by,
                        'latest_updated_by': latest_updated_by,
                    }
        fte = {}

        for column in fte_columns:
            value = get(row, column)
            if value:
                fte[column[-4:]] = value

        stkt_data['fte'] = fte

        other_names = [name.strip() for name in get(row, 'Alternativt namn').split(',')]
        stkt_data['other_names'] = other_names if other_names != [''] else []

        agencies[name] = stkt_data

    return agencies
