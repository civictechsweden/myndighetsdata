import pandas as pd

FILEPATH = "raw_files/agv.csv"

def extract():
    df = pd.read_csv(FILEPATH, delimiter="\t", encoding="utf-16le")
    df["Kön"]= df["Kön"].str.replace("Kvinnor", "women").str.replace("Män", "men")
    agencies = {}

    for agency, agency_df in df.groupby("Nytt namn"):
        if agency not in agencies:
            agencies[agency] = {"total": {}, "women": {}, "men": {}}

        # Process each gender
        for gender, gender_df in agency_df.groupby("Kön"):
            if gender not in ["men", "women"]:
                continue

            for _, row in gender_df.iterrows():
                year = str(row["År"])
                count = row["Valeurs de mesures"]
                agencies[agency][gender][year] = count

                if year not in agencies[agency]["total"]:
                    agencies[agency]["total"][year] = count
                else:
                    agencies[agency]["total"][year] += count

    for agency in agencies:
        for gender in agencies[agency]:
            agencies[agency][gender] = {
                k: agencies[agency][gender][k]
                for k in sorted(agencies[agency][gender].keys(), reverse=True)
            }

    return agencies
