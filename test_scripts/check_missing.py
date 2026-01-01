from utils import read_json

merged_data = read_json("data/merged.json")

print(f"Found {len(merged_data)} agencies")

# for agency in merged_data:
#     end = False
#     data = merged_data[agency]
#     if 'stkt' not in data:
#         for source in data:
#             if 'end' in data[source]:
#                 end = True

#             if 'expired' in data[source] and data[source]['expired'] is not None:
#                 end = True

#         if not end:
#             print(agency)

for agency in merged_data:
    end = False
    data = merged_data[agency]
    if "handlingar" in data and len(data.keys()) == 1:
        for source in data:
            if "end" in data[source]:
                end = True

            if "expired" in data[source] and data[source]["expired"] is not None:
                end = True

        if not end:
            print(agency)

# for agency in merged_data:
#     data = merged_data[agency]
#     if 'stkt' in data and 'other_names' in data['stkt']:
#         other_names = data['stkt']['other_names']
#         if other_names:
#             print(f'{agency} -> {other_names}')
