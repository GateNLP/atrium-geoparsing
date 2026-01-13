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

# Gazetteer Caching

The `generateHazBin.groovy` file is used to generate the cached internal
representation of a gazetteer for speed and memory efficiancies. More
details and instructions are in the [top level README](../README.md#generating-the-gazetteer-cache).