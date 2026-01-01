from utils import get_all_names, read_json
import pandas as pd

merged_data = read_json("data/merged.json")

print(f"Found {len(merged_data)} agencies")

all_names = get_all_names(merged_data, False)

export = []

for other_name in all_names:
    name = all_names[other_name]

    if name.lower() != other_name.lower():
        print(f"{name} -> {other_name}")
        export.append({"name": name, "other_name": other_name})

pd.DataFrame(export).to_excel("merged.xlsx", index=False)
