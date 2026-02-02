# Dataset Agnostic Geoparsing

## Description

_Geoparsing is the process of extracting geographic locations (places, cities, countries) from unstructured text (like documents, tweets, or articles) and converting them into precise geographic coordinates (latitude/longitude)_

This workflow describes workflow for transforming a geographical dataset (such as Geonames or Pleiades) into an application which can be used for detecting locations in text documents coupled withg a geometric approach to disambiguating.

Whilst the workflow can be used on its own it is also intended that it form parts of larger workflows such as those for text processing produced within the ATRIUM project.


## Contributors
Contributors to the design of the workflow include Mark A. Greenwood (USFD), Diana Maynard (USFD). The implementation was completed by Mark A. Greenwood. 


## Requirements
- The workflow must be able to handle a wide variety of geographic datasources
- Disambiguation of places with the same name (i.e. return a single place not a list of possibilities)

## Workflow Steps

The workflow is implemented as a skeleton [GATE](https://gate.ac.uk) application along with a collection of Python and Groovy scripts. Full details on installing and using the workflow are beyond the scope of this description but can be found along with the code in [this GitHub repository](https://github.com/GateNLP/atrium-geoparsing).

The high-level outline of the workflow is as follows:

1. __Select a geographical dataset.__ Any dataset that contains latitude/longitude coordinates for the placenames it contains can be used within this workflow. Examples include GeoNames, Pleiades, and the Digital Survery of English Place-Names.
2. __Convert the dataset to a gazetteer.__ A dataset is converted to a gazeetter by extracting the pairs of placenames and coordinaates and writing them into a TSV file in the correct format. For example, Athens from Pleiades becomes the following line in the gazetteer:


    ```
    Athens	id=579885	lat=37.97289279405569	lon=23.72464729876415
    ```

    The line is tab separated and contains the name of the place, the ID of the entry within the dataset and its coordinates. Generating this format shoud be trivial regardless of the originating dataset. Example scripts for a number of datasets are proivided in the workflow's GitHub repository.

3. __Package the application.__ Once the gazetteer has been generated then it can be placed within the GATE application folder to turn the skeleton into a complete application.
4. __Run the application.__ The completed application can either by run directlym within the GATE Developer UI or as an ELG webservice (full details are in the README).
