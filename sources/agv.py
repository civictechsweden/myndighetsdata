import pandas as pd

FILEPATH = "raw_files/agv.csv"


def extract():
    df = pd.read_csv(FILEPATH, delimiter="\t", encoding="utf-16le")
    agencies = {}

    for _, agency in df.iterrows():
        agency_name = agency.values[0]

        if agency_name == "Medlem" or type(agency_name) is float:
            continue

        agency_data = (
            agency.iloc[1:].str.replace("\xa0", "", regex=False).dropna().astype(int)
        )

        idx = agency_data.index.astype(str)
        total = agency_data[idx.str.fullmatch(r"\d{4}")]
        women = agency_data[idx.str.endswith(".1")]
        men = agency_data[idx.str.endswith(".2")]

        total.index = total.index.astype(int)
        women.index = women.index.str.replace(".1", "", regex=False).astype(int)
        men.index = men.index.str.replace(".2", "", regex=False).astype(int)

        agencies[agency_name] = {
            "total": total.to_dict(),
            "women": women.to_dict(),
            "men": men.to_dict(),
        }

    return dict(sorted(agencies.items()))
