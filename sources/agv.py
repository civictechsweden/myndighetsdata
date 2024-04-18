import pandas as pd

FILEPATH = 'raw_files/agv.xlsx'

def extract():
    years = pd.read_excel(FILEPATH, nrows=0)
    years = [column for column in years.columns.to_list() if column.isdigit()]

    df = pd.read_excel(FILEPATH, header=2)

    agencies = {}

    for _, row in df.iterrows():
        name = row.iloc[0]

        if name in ['Medlem', 'Okänd'] or name != name:
            continue

        agv_data = {}

        for i, year in enumerate(years):

            ext = ''

            if i > 0:
                ext = f'.{i}'

            total = row.loc[f'Totalsumma{ext}']
            women = row.loc[f'Kvinnor{ext}']
            men = row.loc[f'Män{ext}']

            if total != total:
                continue

            agv_data.setdefault('total', {})[year] = int(total)
            agv_data.setdefault('women', {})[year] = int(women) if women == women else 0
            agv_data.setdefault('men', {})[year] = int(men) if men == men else 0

        active_years = list(agv_data['total'].keys())

        if active_years[-1] != years[-1]:
            agv_data['start'] = active_years[-1]

        if active_years[0] != years[0]:
            agv_data['end'] = active_years[0]

        agencies[name] = agv_data

    return agencies
