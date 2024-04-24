# Indexify Local

Indexify, but local.

## Getting Started

### The Environment

To set up the environment, run the following command:

```
$ source start_env
```

## Setup Indexify

To run the setup process, use the following command:

```
$ python indexify-local.py --setup
```

This command will execute the `indexify-local/get_latest` script and download the `all_extractors.json` file.

### Populate Local Extractors
`indexify-local/extractors-json/local_extractors.json`
`indexify-local/extractors-json/local_extractors.json`

After running the setup process, you should populate the `local_extractors.json` file with your preferred extractors from the `all_extractors.json` file. This will be used to generate the supervisor config in the next step. 

```json
[
  {
    "type": "embedding", 
    "module_name": "clip_embedding.openai_clip_extractor:ClipEmbeddingExtractor"
  },
]
```

### Generate supervisord.conf

After creating your `local_extractors.json` generate the supervisord.conf

```
$ python indexify-local.py --make-conf
```

### Starting Indexify-Local

To start Indexify Local, use the following command:

```
$ python indexify-local.py --start
```

### Note: Folder Permissions

Folder permissions should be fine but if you have issues you can ensure `_local_data` and `_watch_folder` directories have the necessary read and write permissions by using `Utils/_local_folders_permissions`.


## Usage

```
usage: indexify-local.py [-h] [--all-extractors] [--local-extractors] [--start [SCRIPT]] [--setup] [--make-conf]

Extractor Downloader

optional arguments:
  -h, --help         show this help message and exit
  --all-extractors   Download all extractors from the default GitHub URL
  --local-extractors Download extractors from the default local JSON file (local_extractors.json)
  --start [SCRIPT]   Path to the bash script to execute (default: run start_env and start_xfi)
  --setup            Run the setup process (get_latest script and download all_extractors.json)
  --make-conf        Generate supervisord.conf based on local-extractors.json
```


## Directory Structure

- `indexify-local/`: Directory containing the Indexify Local files
  - `extractors-json/`: Directory to store the JSON files for extractors
    - `all_extractors.json`: JSON file containing all extractors downloaded from the default GitHub URL or a specified URL
    - `local_extractors.json`: JSON file containing extractors to be downloaded locally
  - `get_latest`: Script to get the newest indexify binary for your system. 