import argparse
import csv
import sys
from tqdm import tqdm
from pathlib import Path

from zipfile import ZipFile
import urllib.request
from io import TextIOWrapper

import unicodedata

import logging

logger = logging.getLogger(__name__)

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

def rows(reader, expand_ascii=True):
    
    count = 0
    for row in tqdm(reader, total=40000): # approx size of biggest country
        try:

            lat = row[-2]
            lon = row[-1]
            
            # no point keeping stuff without valid coordinates
            if lat == "0.0" and lon == "0.0":
                continue

            alt_names = set()
            alt_names.add(row[1])
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
                    f"lat={lat}",
                    f"lon={lon}"
                ]
        except Exception as e:
            print(e, row)
            count += 1
    print('Exception count:', count)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="ATRIUM Engliosh Place-Names Gazetteer Generator")

    parser.add_argument("-i","--input",
        help="Location of CSV file downloaded from English Place-Names")

    parser.add_argument("-o", "--output", default="./locations.lst",
        help="TSV file to write gazetteer into")

    args = parser.parse_args()

    datafile = Path(args.input)
    
    if not datafile.exists():
        logger.error("input data file does not exist")
    else:
        with open(datafile, 'rb') as txtfile:
            reader = csv.reader(TextIOWrapper(txtfile,'utf-8'), delimiter=',')
            next(reader, None)  # skip the headers

            with open(args.output, "w", encoding="utf-8") as outfile:
                writer = csv.writer(outfile, delimiter='\t')

                writer.writerows(rows(reader))
