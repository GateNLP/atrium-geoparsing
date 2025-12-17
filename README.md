# ATRIUM Geoparsing

_Geoparsing is the process of extracting geographic locations (places, cities, countries) from unstructured text (like documents, tweets, or articles) and converting them into precise geographic coordinates (latitude/longitude)_

## Approach Overview

This repository holds a generic [GATE](https://gate.ac.uk/) application for
performing geoparsing. The approach is agnostic to the dataset used making it
possible to quickly and easily build applications which can support different
datasets for different use cases.

The approach is split into two main phases, finding locations in text, and then
disambiguating them against a given dataset. Both phases are described in more
detail below.


### Finding Locations

Many other approaches to geoparsing start by using a general purpose named
entity recogniser (such as [spaCy](https://spacy.io/), or
[NameTag](https://ufal.mff.cuni.cz/nametag/3)) to find text spans that are
assumed to be a location. Unfortunately we have found that this does not
always work as well as expected, especially when considering historical place
names. Any location not identified at this stage can never be linked to a given
dataset and so this places an upper limit on performance of the pipeline as a
whole.

For this reason we flip the problem around and use a simple gazeetteer based 
approach to find locations within text. Essentially we take a given dataset
and extract all possible location names from it which we turn into a
gazetteer ([see below for details](#gazetteer-generation)). This gazetteer is then
used to find all possible candidates in a document. This approach guarantees
high recall, but may suffer from slightly lower precision where a place name
is also a common word -- the application takes some steps to address this by
only considering those candidates which appear to be nouns given the
surrounding context.


### Disambiguation

Whilst in some cases a name may only link to one entry in a given dataset there
are many cases where a name can refer to multiple places. In such a situation
we need to disambiguate these to select the correct entry.

We are currently using a geometric approach to disambiguation which is partially
inspired by the idea of one sense per discourse when doing word sense
disambiguation. In this case we assume that most documents are talking about
locations which occur within a short distance of one another. This allows us to
disambiguate by picking the set of locations which minimise the total area
covered by the bounding box covering the selected points.

Our approach to this uses axis aligned bounding boxes to determine the area
covered by a set of points (more efficient than trying to compute the convex
hull). Ideally we would check every possible combination of points to find the
best fit, but on documents which contain even a medium number of locations this
gets computationally expensive very quickly. Instead we make an initial
selection and then iterate to check each point in turn to look for a better
fit. We continue doing that until we settle on a set of points for which no
better solution can be found. This guarantees finding a local minimum in the
search space but doesn't guarantee the best fit and is determined by the
initial choice of points.


## Customizing the Application

As mentioned above this repository is a generic starting point that can be used
with any relevant dataset. As such it does not contain any place data and this
needs to be provided by the user depending on their needs and use case.

### Gazetteer Generation

Customizing the application essentially invovles converting a given dataset
into a gazetteer which needs to be stored as
`./application-resources/gazetteer/locations.lst`

The format of the gazetteer is fairly straightforward and easy to generate.
As an example, here is an entry for Athens generated from the Pleiades dataset:

```
Athens	id=579885	lat=37.97289279405569	lon=23.72464729876415
```

As you can see the data is stored as a TSV (tab separated values) file, with
the place name in the first column. Each of the other columns then contains a
key/value pair separated by an `=`. Here we have shown a minimal example with
just the ID of the entry in Pleiades and the lat/lon coordinates. You can add
any other columns you wish and they will end up as part of the output. For
example, it might be useful to add a URI column to provide a fully specified
link to the resources; in this case that would be
`https://pleiades.stoa.org/places/579885`.