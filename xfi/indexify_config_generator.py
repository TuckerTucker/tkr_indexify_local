import os

def create_indexify_config(template_path, output_path):
    """
    Generate the Indexify configuration file based on the provided template.

    Args:
        template_path (str): Path to the template file.
        output_path (str): Path to save the generated configuration file.
    """
    try:
        # Read the template file
        with open(template_path, 'r') as template_file:
            template_content = template_file.read()

        # Get the full path of the destination directory's parent directory
        destination_dir = os.path.dirname(os.path.abspath(os.path.dirname(output_path)))

        # Replace the '../' placeholders with the full path of the destination directory's parent directory
        updated_content = template_content.replace('../', destination_dir + '/')

        # Create the output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Write the updated content to the output file
        with open(output_path, 'w') as output_file:
            output_file.write(updated_content)

        print(f"Indexify configuration file created at: {output_path}")
    except FileNotFoundError as e:
        print(f"Template file not found: {template_path}")
        print(f"Error: {e}")
    except IOError as e:
        print(f"Error writing to file: {output_path}")
        print(f"Error: {e}")