import argparse
import csv
import sys
from tqdm import tqdm
from pathlib import Path

from zipfile import ZipFile
import urllib.request
from io import TextIOWrapper

import unicodedata

# this is lifted from textacy.preprocessing.remove as we don't need the
# whole package and it's dependencies for something so trivial
def remove_accents(text: str, *, fast: bool = False) -> str:
    """
    Remove accents from any accented unicode characters in ``text``, either by
    replacing them with ASCII equivalents or removing them entirely.

    Args:
        text
        fast: If False, accents are removed from any unicode symbol
            with a direct ASCII equivalent; if True, accented chars
            for all unicode symbols are removed, regardless.

            .. note:: ``fast=True`` can be significantly faster than ``fast=False``,
               but its transformation of ``text`` is less "safe" and more likely
               to result in changes of meaning, spelling errors, etc.

    Returns:
        str

    See Also:
        For a more powerful (but slower) alternative, check out ``unidecode``:
        https://github.com/avian2/unidecode
    """
    if fast is False:
        return "".join(
            char
            for char in unicodedata.normalize("NFKD", text)
            if not unicodedata.combining(char)
        )
    else:
        return (
            unicodedata.normalize("NFKD", text)
            .encode("ascii", errors="ignore")
            .decode("ascii")
        )

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

def rows(reader, expand_ascii=True):
    
    count = 0
    for row in tqdm(reader, total=12237435): # approx
        try:
            alt_names = set()
            alt_names.add(row[1])
            alt_names.add(row[2])
            alt_names.update(set(row[3].split(",")))
            alt_name_length = len(alt_names)
            if expand_ascii:
                alt_names.update([remove_accents(i) for i in alt_names])
                
            # why is this necessary at all?
            alt_names.discard("")
            alt_names.discard(None)
            
            for name in alt_names:
            
                if len(name) < 4:
                        continue
                        
                yield [
                    name,
                    f"id={row[0]}",
                    f"lat={row[4]}",
                    f"lon={row[5]}"
                ]
        except Exception as e:
            print(e, row)
            count += 1
    print('Exception count:', count)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="ATRIUM Geonames Gazetteer Generator")

    parser.add_argument("-i","--input", default="./allCountries.zip",
        help="Location of the Geonames data file")

    parser.add_argument("-o", "--output", default="./locations.lst",
        help="TSV file to write gazetteer into")

    args = parser.parse_args()

    datafile = Path(args.input)
    
    if not datafile.exists():
        download_url('https://download.geonames.org/export/dump/allCountries.zip',datafile)

    with ZipFile(datafile) as zf:
        with zf.open("allCountries.txt", 'r') as txtfile:
            reader = csv.reader(TextIOWrapper(txtfile,'utf-8'), delimiter='\t')

            with open(args.output, "w", encoding="utf-8") as outfile:
                writer = csv.writer(outfile, delimiter='\t')

                writer.writerows(rows(reader))
