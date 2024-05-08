# Basic Python Virtual Envirionment Set Up
 Automatically sets up a Python virtual environment. 

## What it does


Run the script

    ```bash
    source tkr_env.sh
    ```

    or move this outside of tkr_env folder (into your project folder)
    start_env.MoveThisUpOneDirectory
    and remove the .MoveThisUpOneDirectory

    ```bash
    source start_env
    ```    

    
1. First it checks if the environment exists.
env true: Creates and activates the environtment then installs all packages in 'env_requirements' (listed below). 
env false: Activates the environment.

### Change Environment Nmme
Set the `env_name` variable in `tkr_env.sh` to customize the name of the virtual environment before it's created.
*To change the environment name after it's created you'll need to do it manually.*
*It's easiest to just delete the project_env folder and restart with a new name.*