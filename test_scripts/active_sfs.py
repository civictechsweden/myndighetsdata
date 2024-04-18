from utils import read_json

sfs = read_json('data/sfs.json')
stkt = read_json('data/stkt.json')
stkt_lower = [agency.lower() for agency in stkt]

for agency in sfs:
    if not sfs[agency]['expired'] and agency.lower() not in stkt_lower:
        print(agency)
