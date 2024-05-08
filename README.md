# Indexify Local

Indexify Local provides a streamlined way to manage and run local extractors for data processing. This guide will help you set up and use Indexify Local on your machine.

## Getting Started

### Prerequisites

Before you begin, ensure you have Python and Node.js installed on your system. You will also need `pip` for Python dependencies and `npm` for Node.js packages.

### Environment Setup

To set up the environment, execute the following command:

```bash
source start_env
```

This script initializes the necessary environment variables and activates the virtual environment.

## Installation

### Install Python Dependencies

Install the required Python packages by running:

```bash
pip install -r requirements.txt
```

### Install UI Dependencies

Navigate to the UI directory and install the necessary Node.js packages:

```bash
cd ui
npm install
```

### Add Local Recipe

To add a new local recipe, use the following command:

```bash
--new-local whisper_chain.json
```

## Setup Indexify Local

### Initial Setup

Run the setup process with this command:

```bash
python xfi-local.py --setup
```

This will execute the `indexify-local/get_latest` script and download the `all_extractors.json` file.

### Populate Local Extractors

Edit the `local_extractors.json` file to include your preferred extractors from the `all_extractors.json` file:

```json
[
  {
    "type": "embedding",
    "module_name": "clip_embedding.openai_clip_extractor:ClipEmbeddingExtractor"
  }
]
```

### Configuration Files

Generate the `indexify.init.config` file:

```bash
python indexify-local.py --make-init-config
```

Then, generate the `supervisord.conf` file:

```bash
python indexify-local.py --make-conf
```

### Starting Indexify Local

To start Indexify Local, use the following command:

```bash
python indexify-local.py --start
```

### Folder Permissions

Ensure the `_local_data` and `_watch_folder` directories have the necessary permissions:

```bash
Utils/_local_folders_permissions
```

## Usage

Here are the available commands for managing Indexify Local:

```bash
usage: indexify-local.py [-h] [--all-extractors] [--local-extractors] [--start [SCRIPT]] [--setup] [--make-conf] [--make-init-config]

optional arguments:
  -h, --help           show this help message and exit
  --all-extractors     Download all extractors from the default GitHub URL
  --local-extractors   Download extractors from the default local JSON file (local_extractors.json)
  --start [SCRIPT]     Path to the bash script to execute (default: run start_env and start_xfi)
  --setup              Run the setup process (get_latest script and download all_extractors.json)
  --make-conf          Generate supervisord.conf based on local-extractors.json
  --make-init-config   Generate indexify.init.config based on the template
```