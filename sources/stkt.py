from utils import get, get_sfs
import urllib.request
import pandas as pd
import ssl
import certifi

ssl._create_default_https_context = lambda: ssl.create_default_context(
    cafile=certifi.where()
)


URL = "https://www.statskontoret.se/siteassets/dokument/exceldokument/statskontorets-myndighetsforteckning---2025-.xlsx"
FILEPATH = "raw_files/stkt.xlsx"


def download():
    urllib.request.urlretrieve(URL, FILEPATH)


def extract():
    agencies = {}

    df = pd.read_excel(FILEPATH, "Förteckning 2007-2025")

    df["sfs"] = df["sfs"].apply(get_sfs)
    df["senaste_sfs"] = df["senaste_sfs"].apply(get_sfs)

    def non_null(x, pos=-1):
        x = x.dropna()
        return x.iloc[pos] if len(x) > 0 else ""

    def year_value_dict(values, years):
        s = (
            pd.DataFrame({"år": years, "val": values})
            .dropna(subset=["val"])
            .sort_values("år")
        )
        return dict(zip(s["år"].astype(int), s["val"]))

    df_sorted = df.sort_values("år")

    df_cleaned = df_sorted.groupby("orgnr", as_index=False).agg(
        {
            "myndighet": non_null,
            "alternativt_namn": lambda x: list(pd.unique(x.dropna())),
            "cofog": non_null,
            "cofog_10": non_null,
            "värdmyndighet": non_null,
            "departement": non_null,
            "ledningsform": non_null,
            "affärsverk": lambda x: non_null(x) == "Affärsverk",
            "insynsråd": lambda x: non_null(x) == 1,
            "myndighetschef": non_null,
            "överdirektör": lambda x: non_null(x) == 1,
            "sfs": lambda x: non_null(x, 0),
            "senaste_sfs": lambda x: non_null(x, 0),
            "årsarbetskrafter": lambda x: year_value_dict(
                x, df_sorted.loc[x.index, "år"]
            ),
        }
    )

    for _, row in df_cleaned.iterrows():
        name = get(row, "myndighet")

        agencies[name] = {
            "department": get(row, "departement"),
            "org_nr": str(get(row, "orgnr")),
            "cofog": get(row, "cofog"),
            "cofog10": get(row, "cofog_10"),
            "host": get(row, "värdmyndighet"),
            "structure": get(row, "ledningsform"),
            "has_gd": str(get(row, "myndighetschef")) == "1",
            "created_by": get(row, "sfs"),
            "latest_updated_by": get(row, "senaste_sfs"),
            "fte": get(row, "årsarbetskrafter"),
            "other_names": get(row, "alternativt_namn"),
        }

    return dict(sorted(agencies.items()))
