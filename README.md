# Myndighetsdata

![A wise owl that knows everything about government agencies](./illustration.webp)

Myndighetsdata is an attempt to make data about the Swedish government agencies (*myndigheter*) more accessible. By data, I mean name and basic information such as contact details, address... It downloads the data from various sources, converts it to structured JSON files with a consistent format and even attempts to merge all these data points in one big list.

There are many government agencies in Sweden, they get called by various names and several hundred agencies have disappeared over the past decades. This data will hopefully be of some help to those who try to study public sector and build services building on government data. It's not a finished product, it's not 100% clean and exact but feel free to reuse it and contribute to make it even better! 😊

I recommend to read [my blog post](https://medium.com/civictechsweden/vem-har-koll-på-sveriges-myndigheter-dc8ca8e9dab7) to get a better overview of the different sources' strengths and weaknesses.

## Where is the data?

It's in the [data](./data) folder:

- [agv.json](./data/agv.json) is data from [Arbetsgivarverket](https://www.arbetsgivarverket.se/statistik-och-analys/staten-i-siffror-anstallda-i-staten/staten-i-siffror-om-arbetsgivarverkets-medlemmar)
- [esv.json](./data/esv.json) comes from Ekonomistyrningsverket's [myndighetsregister](https://www.esv.se/rapportering/myndighetsregistret/)
- [handlingar.json](./data/handlingar.json) comes from [handlingar.se](https://handlingar.se)
- [scb.json](./data/scb.json) combines SCB's [myndighetsregister](https://myndighetsregistret.scb.se) with the [information about added and removed agencies](https://myndighetsregistret.scb.se/Ar)
- [sfs.json](./data/sfs.json) extracts agency names from the government's [rättsdatabas](https://beta.rkrattsbaser.gov.se)
- [stkt.json](./data/stkt.json) comes from Statskontoret's [list](https://www.statskontoret.se/fokusomraden/fakta-om-statsforvaltningen/myndigheterna-under-regeringen/)
- [wd.json](./data/wd.json) comes from [Wikidata](https://www.wikidata.org)

And [merged.json](./data/merged.json) is an attempt at merging all these files together by matching agencies by organisation numbers and by name (using fuzzy matching and some wild rules). It is not 100% correct as the underlying data is too unconsistent. But it can be used in order to complete Wikidata and improve the quality of government sources so that future merge attempts are easier.

As of today, the data is collected manually every once in a while (2-3 times a year) so things such as instruction or number of employees might be outdated.

## How to run the code

You can use the code yourself to download the source files, extract the information from them and merge it.

For this, you need Python 3 and to install dependencies:

```bash
pip install -r requirements.txt
```

Once that is done, you can run the following commands:

```bash
# Download the source files (if DOWNLOAD is set to True) and extract the information from them
python run.py
# OBS: Arbetsgivarverket's data has to be downloaded manually

# Try to merge the lists into one
python smart_merge.py

# Rule-based cleaning to remove the biggest anomalies in the merged file
python manual_cleaning.py

# Generate a list of all possible names of all agencies. The result is saved as matchlist.csv
# and can be used to find a certain agency even when it's not referred to by its official name.
python generate_matchlist.py
```

## License

The code is licensed under AGPLv3, which means you can reuse as long as you attribute, and that you can modify as long as you published what you make.

The data comes from a number of sources but they are all licensed as CC0, either explicitly or through praxis (*allmänna handlingar* can usually be considered CC0). So feel free to reuse as you please!
