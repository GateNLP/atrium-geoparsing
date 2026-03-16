# Gazetteer Generation Scripts

This folder contains a number of scripts for generating a GATE gazetteer file
which can be used by the ATRIUM Geoparsing GATE app. The scripts all operate
in roughly the same fashion.

Running a script (in a Python environment with the relevant modules installed)
will download the required dataset, process it and produce a `locations.lst`
file in the current direcotry. _Note this means that running scripts in
sequence will trample on the output of previous scripts._

Once you have generates a `locations.lst` for the dataset you are interested in
you can move it into `../application-resources/gazetteer/` in order to complete
the GATE app ready for use.

Note that if you want to use different input/output files then the scripts
accept command line options `-input` and `--output` which allow you to do so.

## English Place-Names

Note that generating a gazetteer from the English Place-Names data is a little
more involved as it isn't currently possible to automatically download the
complete dataset; in fact you can't even download the whole dataset in one
go manually.

Currently the best way to download the data from
[English-Place Names](https://sepn.nottingham.ac.uk/view-only/data/placenames/) is
one county at a time. You can restrict the results by county in the search box
on the right of the results display. If you then select the first page of results
(check the box at the left of the header row), you will then be given the option
to select all matching records. Once these have been selected you can then choose
to "Export to CSV" from the actions drop down. This can take a moment or two to
respond; it will timeout on the whole dataset, but will manage Cheshire which is
I believe the largest county, so will allow the county-by-county approach.

Once you have downloaded the county file you can then proces it using the provided
`epn_gaz_gen.py` script. If you generate a `.lst` file for each county you can
then simply append these together to produce a single `locations.lst` file for
the complete dataset.

# Gazetteer Caching

The `generateHazBin.groovy` file is used to generate the cached internal
representation of a gazetteer for speed and memory efficiancies. More
details and instructions are in the [top level README](../README.md#generating-the-gazetteer-cache).
