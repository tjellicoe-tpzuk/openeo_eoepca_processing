# CWL application to load a STAC item using the openEO package and computing NDVI

### Python

Containerised Python script to load STAC data using openEO functions and compute NDVI for the dataset

### CWL

Python script is containerised using Docker and wrapper in a CWL script allowing it to be called from the Command Line with the URL or file path of a STAC item.

### How to use

To run this CWL script open a terminal in the repository and run the following command `cwltool get-eo-data-wrkflw.cwl#run_openeo --dataSet <STAC_item_url>`

A good example STAC item is available at https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/S2A_38VNM_20221124_0_L2A.

### Using with the ADES

This CWL script defines an OGC Application Package which can be executed using any CWL running. Of particular note is the interfacing with [EOEPCA](https://deployment-guide.docs.eoepca.org/latest/). With a running EOEPCA instance, either local or cloud deployed, you can pass in the URL of the raw CWL script along with the URL of a STAC item and see the NDVI computation returned.
