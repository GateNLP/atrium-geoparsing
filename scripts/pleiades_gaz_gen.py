import argparse
import urllib.request


import bigjson
import csv
import gzip


from tqdm import tqdm
from pathlib import Path


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)


def rows(reader):

    total = 0
    missed = 0
    unlocated = 0

    pleiades = bigjson.load(reader)["@graph"]
    
    for element in tqdm(pleiades, total=41480): # valid as of May 2025
        total += 1
    
        if element['reprPoint'] is None:
            unlocated += 1
            continue
            
        #print(element["id"])
        
        lat = element['reprPoint'][1]
        lon = element['reprPoint'][0]

        
        for name in element["names"]:
            alt_names = set()
            alt_names.add(name["attested"])                    
            alt_names.update([x.strip() for x in name["romanized"].split(',')])
                    
            # why is this necessary at all?
            alt_names.discard("")
            alt_names.discard(None)

            for entry in alt_names:
            
                # this ensures all whitespace is normalised to a single space
                entry = ' '.join(entry.split())
            
                # this causes us to skip over numbers
                try:
                    num = float(entry)
                    continue
                except ValueError:
                    pass
            
                # feels slightly arbitrary but....
                if len(entry) < 4:
                    continue
            
                yield [
                    entry,
                    "id="+element["id"],
                    "lat="+str(lat),
                    "lon="+str(lon),
                    "start="+str(name["start"]),
                    "end="+str(name["end"]),
                    "lang="+("" if name["language"] is None else name["language"])
                ]

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="ATRIUM Pleiades Gazetteer Generator")

    parser.add_argument("-i","--input", default="./pleiades-places-latest.json.gz",
        help="Location of the Pleiades data file")

    parser.add_argument("-o", "--output", default="./locations.lst",
        help="TSV file to write gazetteer into")

    args = parser.parse_args()

    datafile = Path(args.input)
    
    if not datafile.exists():
        download_url('https://atlantides.org/downloads/pleiades/json/pleiades-places-latest.json.gz',datafile)

    with gzip.open(datafile,'rt', encoding='utf-8') as reader:
        with open(args.output, 'w', newline='') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
            for row in rows(reader):
                writer.writerow(row)
