from utils import write_json

import sources.esv as esv
import sources.stkt as stkt
import sources.scb as scb
import sources.wikidata as wd
import sources.sfs as sfs
import sources.agv as agv
import sources.handlingar as handlingar

DOWNLOAD = False

if DOWNLOAD:
    print('Downloading from ESV...')
    esv.download()
print('Extracting from ESV...')
esv_data = esv.extract()
write_json(esv_data, 'esv')

if DOWNLOAD:
    print('Downloading from Statskontoret...')
    stkt.download()
print('Extracting from Statskontoret...')
stkt_data = stkt.extract()
write_json(stkt_data, 'stkt')

if DOWNLOAD:
    print('Downloading from SCB...')
    scb.download()
print('Extracting from SCB...')
scb_data = scb.extract()
write_json(scb_data, 'scb')

if DOWNLOAD:
    print('Downloading from Wikidata...')
    wd.download()
print('Extracting from Wikidata...')
wd_data = wd.extract()
write_json(wd_data, 'wd')

if DOWNLOAD:
    print('Downloading from SFS...')
    sfs.download()
print('Extracting from SFS...')
sfs_data = sfs.extract()
write_json(sfs_data, 'sfs')

print('Extracting from Arbetsgivarverket...')
agv_data = agv.extract()
write_json(agv_data, 'agv')

if DOWNLOAD:
    print('Downloading from Handlingar...')
    sfs.download()
print('Extracting from Handlingar...')
handlingar_data = handlingar.extract()
write_json(handlingar_data, 'handlingar')
