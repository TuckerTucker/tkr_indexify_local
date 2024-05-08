#!/bin/bash

# Function to display help message
display_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  -h, --help           Display this help message"
    echo "  --env-name NAME      Specify the name of the virtual environment (default: indexify_env). If you change it be sure to update the .gitignore"
    echo "  --python-path PATH   Specify the directory to add to the Python path"
    echo "  --base-dir PATH      Specify the base directory path (default: current directory)"
}

# Function to check and add Python path
add_python_path() {
    if [ -n "$python_path" ]; then
        if echo "$PYTHONPATH" | grep -q "\(^\|:\)$python_path\(:\|$\)"; then
            echo -e "\e[38;5;208m$python_path \nis already in PYTHONPATH.\e[0m"
        else
            echo -e "\e[38;5;208mAdding $python_path to PYTHONPATH\e[0m"
            export PYTHONPATH="$python_path:$PYTHONPATH"
        fi
    fi
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -h|--help)
            display_help
            exit 0
            ;;
        --env-name)
            env_name="$2"
            shift
            shift
            ;;
        --python-path)
            python_path="$2"
            shift
            shift
            ;;
        --base-dir)
            base_dir="$2"
            shift
            shift
            ;;
        *)
            echo "Unknown option: $1"
            display_help
            exit 1
            ;;
    esac
done

# Set default values if not provided
env_name=${env_name:-project_env} # 'project_env' is the default name
base_dir=${base_dir:-$(pwd)} # adds the current working directory as base directory. Use call the script from outside of 
python_path=${python_path:-$base_dir/indexify-extractors}

# Check if the virtual environment already exists
if [ -d "$env_name" ]; then
    source "$env_name/bin/activate"
    echo -e "\e[38;5;208mActivated '$env_name'.\e[0m"
    
    # Call the function to check and add Python path
    # add_python_path
else
    # Create the virtual environment if it does not exist
    python3 -m venv $env_name
    echo -e "\e[38;5;208mCreated '$env_name'.\e[0m"

    # Define a timeout in seconds and polling interval (e.g., half a second)
    timeout=300
    elapsed=0
    poll_interval=0.5
    pip_interval=1

    # Check if the activation script exists, with polling
    while [ $elapsed -lt $timeout ]; do
        if [ -f "$env_name/bin/activate" ]; then
            source "$env_name/bin/activate"
            echo -e "\e[38;5;208mActivated '$env_name'.\e[0m"

            # Check if the virtual environment is correctly activated
            if [[ -z "$VIRTUAL_ENV" ]]; then
                echo -e "\e[38;5;201mThe virtual environment is not activated properly. Please check the environment.\e[0m"
                break
            else
                # Install requirements from env_requirements
                echo -e "\e[38;5;208mInstalling requirements from env_requirements\e[0m"
                #pip install --no-cache-dir -r -q "env_requirements" > /dev/null 2>&1 &
                pip install --no-cache-dir -r "env_requirements" > /dev/null 2>&1 &

                while kill -0 $! 2> /dev/null; do
                    echo -n '. '
                    sleep $pip_interval
                done
                echo "\n"

                # Call the function to check and add Python path
                # add_python_path
            fi
            break
        else
            echo -e "\e[38;5;208mWaiting for the virtual environment to be ready...\e[0m"
            sleep $poll_interval
            elapsed=$(echo "$elapsed + $poll_interval" | bc)
        fi
    done
fi

# Check if the virtual environment is activated
if [[ -n "$VIRTUAL_ENV" ]]; then
    echo -e "\e[38;5;208mVirtual environment '$env_name' is activated.\e[0m"
else
    echo -e "\e[38;5;201mFailed to activate the virtual environment '$env_name'.\e[0m"
    exit 1
fi