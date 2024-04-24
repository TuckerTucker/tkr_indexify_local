# Basic Python Virtual Envirionment Set Up

 Automatically sets up a Python virtual environment, checks the availability of a local LM Studio server, and falls back to OpenAI's API if the local server is not available. The project includes scripts for environment setup and server interaction, making it easy to start experimenting with LLMs.


## What it does

Run the script

    ```bash
    source tkr_env.sh
    ```

1. First it checks if the environment exists.
No environment? - Creates and activates the environtment then installs all packages in 'requirements' (listed below). 
Environment? - Activates the environment.

### Change Environment Nmme
Set the `env_name` variable in `tkr_env.sh` to customize the name of the virtual environment before it's created.
*To change the environment name after it's created you'll need to do it manually.*
*It's easiest to just delete the project_env folder and restart with a new name.*