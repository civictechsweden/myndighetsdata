import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

from utils import get, remove_parenthesis

DOMAIN = 'https://myndighetsregistret.scb.se'

GROUPS = [
    'Statliga förvaltningsmyndigheter',
    'Myndigheter under riksdagen',
    'Statliga affärsverk',
    'AP-fonder',
    'Sveriges domstolar samt Domstolsverket',
    'Svenska utlandsmyndigheter'
]

URL = '/myndighet/download?myndgrupp={}&format=True'

HISTORY_URL = {
    'start': '/Ar/HamtaNyaMynd',
    'end': '/Ar/HamtaNedMynd'
}

FOLDER = 'raw_files/scb/'
FILEPATH = FOLDER + '{}.xlsx'

def download():
    for group in GROUPS:
        r = requests.get(DOMAIN + URL.format(group))
        with open(FILEPATH.format(group), 'wb') as outfile:
            outfile.write(r.content)

    start_data = download_history('start')
    end_data = download_history('end')
    start_data.update(end_data)

    with open(FOLDER + 'history.json', 'w', encoding='utf-8') as file:
        json.dump(start_data, file, indent=2, ensure_ascii=False)

def download_history(start_or_end):
    agencies = {}

    for year in range(2008, datetime.now().year + 1):
        agent = 'Myndighetsbot/0.1 (http://github.com/PierreMesure/better_myndighetsregister)'
        headers = { 'User-Agent': agent}
        r = requests.post(
                        DOMAIN + HISTORY_URL[start_or_end],
                        data = {'ar': year},
                        headers = headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        tds = soup.find_all('td')

        for i in range(1, len(tds), 2):
            name, short_name = remove_parenthesis(tds[i].text)
            name = name.strip()

            org_nr = tds[i - 1].text

            if name not in agencies:
                agency = { 'org_nr': org_nr }

            agency[start_or_end] = year

            if short_name:
                agency['short_name'] = short_name

            agencies[name]= agency

    return agencies

def extract():
    agencies = {}
    org_nrs = []

    for group in GROUPS:
        df = pd.read_excel(FILEPATH.format(group))

        for _, row in df.iterrows():
            name = get(row, 'Namn')
            name, short_name = remove_parenthesis(name)
            name = name.strip()

            if not name:
                continue

            org_nr = get(row, 'Organisationsnr')

            address = get(row, 'PostAdress')
            if address == '':
                address = ' '.join(get(row, f'PostAdress{i}') for i in range(1, 7))
                postal_address = { 'address' : address.strip() }
            else:
                postal_address = {
                    'address': address,
                    'postcode': get(row, 'PostNr'),
                    'city': get(row, 'PostOrt')
                }

            address = get(row, 'BesöksAdress')
            postcode = get(row, 'BesöksPostNr')

            if address == '' and postcode == '':
                address = ' '.join(get(row, f'BesöksAdress{i}') for i in range(1, 8))
                office_address = { 'address' : address.strip() }
            else:
                office_address = {
                    'address': address,
                    'postcode': get(row, 'BesöksPostNr'),
                    'city': get(row, 'BesöksPostOrt')
                }

            agencies[name] = {
                'org_nr': org_nr,
                'created_by': get(row, 'SFS'),
                'email': get(row, 'Epost'),
                'phone': get(row, 'Tfn'),
                'website': get(row, 'Webbadress'),
                'group': group,
                'postal_address': postal_address,
                'office_address': office_address
            }

            if short_name:
                agencies[name]['short_name'] = short_name

            org_nrs.append(org_nr)

    with open(FOLDER + 'history.json', 'r') as file:
        history = json.load(file)

    ended = [name for name in history if 'end' in history[name]]
    started = [name for name in history if 'start' in history[name]]

    for name in ended:
        org_nr = history[name]['org_nr']

        if org_nr not in org_nrs:
            agencies[name] = history[name]
            org_nrs.append(org_nr)
        else:
            current_name = [agency for agency in agencies
                                if agencies[agency]['org_nr'] == org_nr][0]
            scb_data = agencies[current_name]

            if name.lower() != current_name.lower():
                old_names = scb_data.get('old_names', [])
                if name not in old_names:
                    old_names.append(name)
                    scb_data['old_names'] = old_names

                agencies[current_name] = scb_data

    for name in started:
        org_nr = history[name]['org_nr']

        if org_nr not in org_nrs:
            agencies[name] = history[name]
        else:
            current_name = [agency for agency in agencies
                                if agencies[agency]['org_nr'] == org_nr][0]
            agencies[current_name]['start'] = history[name]['start']

    return agencies
