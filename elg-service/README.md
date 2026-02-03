# Generate an ELG Compliant REST Service

Whilst the GATE application can be used on its own (either via GATE Developer or the GATE Cloud Paralleliser etc.) it is probably more useful as a REST service that can then be easily integrated into other workflows.

To make this as easy as possible we have included within this folder a simple way of packaging up the application as an [ELG](https://european-language-grid.readthedocs.io/) compliant REST service. Whilst [full details on how to construct a compliant REST service](https://european-language-grid.readthedocs.io/en/stable/all/A1_PythonSDK/TutoServiceIntegration.html) are available we are utilizing a [Docker base image from ELG](https://gitlab.com/european-language-grid/usfd/gate-ie-worker) that was specifically designed to wrap GATE applications. In theory this means that if you follow the simple instructions carefully everything should just work.


## Build the GATE Application

The first step in building the ELG REST service is to flesh out the skeleton app provided for the GATE application by building the relevant gazetteer etc. Follow [the instructions in the root of the repository](../README.md) to complete this step.


## Generate the Dockerfile

The next step is to generate the Dockerfile that we will use to build the service, and to collect together all the necessary resources files etc. This is done via an [Apache ANT](https://ant.apache.org/) build file. Assuming you have ANT installed (if not then we recommend using [SDKMAN](https://sdkman.io/)) you can generate the build folder using the command:

```
ant build -Ddataset=<dataset>
```

in which `<dataset>` should be replaced by the name of the dataset you have used for the gazetteer (or some other sensible identifier) -- this allows you to build multiple different images for different datasets etc.

Assuming everything works then you should find a new folder at `./build/atrium-geoparsing-<dataset>` which will contain a `Dockerfile`, `application.yml` and a self contained copy of the GATE application and its dependencies.


## Build the Docker Image

To build the Docker image start by changing into the folder generated in the previous step and then run the command:

```
docker build . -t ${PWD##*/}:latest
```

If, for example, you used `geonames` as the `<dataset>` identifier in the previous step then this would build an image named `atriium-geoparsing-geonames:latest`. Of course you are free to modify this as necessary, especially if you want to push the image to a Docker repository etc. but for now this command will be enough to ensure that

1. the image builds successfully
2. images for different datasets get named differently so that they don't conflict with one another.

## Run and Test the Service

Once you have successfully built the image you can start up the container using the following command:

```
docker run -p 8080:8080 ${PWD##*/}:latest
```

Note that if you edited the image tag in the prevois step then you would need to use a matching tag in this command.

The services exposes the endpoint on port 8080 so this needs to be mapped to an available port on the host machine; here we have simply mapped it onto 8080 (format of the `-p` option is host:container).

Once the container is running you can access the service at `http://localhost:8080/process`. The end point accepts JSON documents in the [ELG Request format](https://european-language-grid.readthedocs.io/en/stable/all/A3_API/LTInternalAPI.html#text-requests), a minimal example of which would be:

```
{
    "type": "text",
    "content": "Where is London?"
}
```

Sending this file (let's assume it's saved as `sample.json` in the current directory) via cURL would involve the following command:

```
curl -X POST -H "Content-Type: application/json" --data @sample.json http://localhost:8080/process
```

which, if everything is working correctly should respond with the following JSON (note some debug field have been removed for clarity):

```
{
  "response": {
    "type": "annotations",
    "annotations": {
      "Location": [
        {
          "start": 9,
          "end": 15,
          "features": {
            "id": "1313003",
            "lat": "25.09229",
            "lon": "96.28854",
          }
        }
      ]
    }
  }
}
```

This response follows the [ELG Annotation Response format](https://european-language-grid.readthedocs.io/en/stable/all/A3_API/LTInternalAPI.html#annotations-response) which gives the offsets within the text for each Location that has been annotated along with the dataset ID linked to and the latitude/longitude coordinates.