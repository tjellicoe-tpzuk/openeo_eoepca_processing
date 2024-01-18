from openeo.local import LocalConnection #from openeo import download_results
import json
from openeo.internal.graph_building import PGNode
import sys
from time import sleep
import math
import os
import time
import mimetypes
import datetime as dt
import xarray as xr

out_dir = os.getcwd()

## this script will take as an input a dataset name for EO data available via Google Earth Engine (https://developers.google.com/earth-engine/datasets/catalog), 
## which it will them compute some complex process using OpenEO in-build processes and return the output STAC catelogue item

testing = False

def main(dataName: str):
   
  #dataName = "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/S2A_38VNM_20221124_0_L2A"
  outName = "stac_loaded"

  local_conn = LocalConnection("./")

  #connection.authenticate_basic("group11", "test123")

  datacube = local_conn.load_stac(dataName)

  ## Extract RED band information
  b04 = datacube.band("B04")
  #print(b04)
  
  ## Extract NIR band information
  b08 = datacube.band("B08")
  #print(b08)

  ## Compute NDVI
  ndvi = (b04-b08) / (b04+b08)

  ## Execute datacube, computing NDVI
  job = ndvi.execute()

  ## To save to a NETCDF, attributes have to be of type string, rather than dictionaries, so we convert them here
  try:
    job.attrs['reduced_dimensions_min_values'] = str(job.attrs['reduced_dimensions_min_values'])
  except:
    None
  try:
    job.attrs['spec'] = str(job.attrs['spec'])
  except:
    None
  try:
    job.attrs['processing:software'] = str(job.attrs['processing:software'])
  except:
    None

  outfile = job.to_netcdf()
  outfile_type = "nc"
  outfile_name = outName


  with open(f"{outfile_name}.{outfile_type}", "wb") as file:
      file.write(outfile)
  file.close()

  createStac(outName, outfile_type)
    
## This needs to be created correctly in future
def createStac(outName, outfile_type):
    createStacItem(outName, outfile_type)
    createStacCatalogRoot(outName, outfile_type)

def createStacItem(outName, outfile_type) :
    now = time.time_ns()/1_000_000_000
    dateNow = dt.datetime.fromtimestamp(now)
    dateNow = dateNow.strftime('%Y-%m-%dT%H:%M:%S.%f') + "Z"
    size = os.path.getsize(f"{outName}.{outfile_type}")
    mime = mimetypes.guess_type(f"{outName}.{outfile_type}")[0]
    data = {"stac_version": "1.0.0",
  "id": f"{outName}-{now}",
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [
        [-180, -90],
        [-180, 90],
        [180, 90],
        [180, -90],
        [-180, -90]
      ]
    ]
  },
  "properties": {
    "created": f"{dateNow}",
    "datetime": f"{dateNow}",
    "updated": f"{dateNow}"
  },
  "bbox": [-180, -90, 180, 90],
  "assets": {
    f"{outName}": {
      "type": f"{mime}",
      "roles": ["data"],
      "href": f"{outName}.{outfile_type}",
      "file:size": size
    }
    },
  "links": [{
    "type": "application/json",
    "rel": "parent",
    "href": "catalog.json"
  }, {
    "type": "application/geo+json",
    "rel": "self",
    "href": f"{outName}.json"
  }, {
    "type": "application/json",
    "rel": "root",
    "href": "catalog.json"
  }]
}
    with open(f'{out_dir}/{outName}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("created")


def createStacCatalogRoot(outName, outfile_type) :
    data = {
  "stac_version": "1.0.0",
  "id": "catalog",
  "type": "Catalog",
  "description": "Root catalog",
  "links": [{
    "type": "application/geo+json",
    "rel": "item",
    "href": f"{outName}.json"
  }, {
    "type": "application/json",
    "rel": "self",
    "href": "catalog.json"
  }]
}
    with open(f'{out_dir}/catalog.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    if testing:
        dataSet = "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/S2A_38VNM_20221124_0_L2A"
    else:
        args = sys.argv
        print(args)
        dataSet = args[4]
    
    main(dataSet)
