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

## Setup Indexify Local

### Initial Setup

Run the setup process using this command:

```bash
python xfi-local.py --setup
```

This will execute the `indexify-local/get_latest` script and download the `all_extractors.json` file.

### Download and Setup Extractors

To download all available extractors from a remote repository, use:

```bash
python xfi-local.py --all-extractors
```

Alternatively, to download specific extractors based on a JSON file:

```bash
python xfi-local.py --local-extractors path_to_your_extractor_file.json
```

### Configuration Files

Generate the `indexify.init.config` and `supervisord.conf` files:

```bash
python xfi-local.py --make-init-config
python xfi-local.py --make-conf
```

### Adding a New Local Extractor Chain

To add a new extractor chain based on a recipe, use the following command:

```bash
python xfi-local.py --new-local path_to_your_recipe.json
```

This command updates the policies and configuration based on the provided recipe.

### Resetting Indexify Local

To reset the environment by removing all logs and configuration files, use:

```bash
python xfi-local.py --reset
```

To clear only the logs:

```bash
python xfi-local.py --clear-logs
```

## Running Indexify Local

### Starting the Server

To start Indexify Local with default scripts:

```bash
python xfi-local.py --start
```

For a custom start script, replace the default with your script:

```bash
python xfi-local.py --start path_to_your_script.sh
```

### Monitoring and Control

Run the process monitor tool if needed:

```bash
./run_supervisord
```

### Check the UI

To see if your extractors and chains are added correctly check the UI

Start the UI:

```bash
./start_ui
```

Access UI at `http://localhost:3000/ui`.

For more details on how to use the UI, please visit:

[Official Indexify UI Help Docs](https://getindexify.com/ui/)