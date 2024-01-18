cwlVersion: v1.0
$namespaces:
  s: https://schema.org/
schemas:
  - http://schema.org/version/9.0/schemaorg-current-http.rdf
s:softwareVersion: 0.1.2

$graph:
  - class: Workflow
    id: run_openeo
    doc: Gathers specified EO data from GEE and applies ndvi process
    label: run OpenEO on Google Earth Engine backend
    inputs:
      dataSet:
        type: string

    outputs:
      outs:
        type: Directory
        outputSource:
          - get_data/outs

    steps:
      get_data:
        run: "#get_data"
        in:
          dataSet: dataSet
        out:
          - outs

  - class: CommandLineTool
    id: get_data
    #main(dataSet, funcName, coords, tempExt, outFileName)
    baseCommand: ["python", "-m", "openeo-load-stac-dask"]
    inputs:
      dataSet:
        type: string
        inputBinding:
          #prefix: --data
          position: 1

    outputs:
      outs:
        type: Directory
        outputBinding:
          glob: .

    requirements:
      DockerRequirement:
        dockerPull: tjellicoetpzuk/openeo-eoepca:latest
      #NetworkAccess:
      #  networkAccess: true
        
