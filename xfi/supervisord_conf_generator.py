import json

def generate_supervisord_conf(input_file, output_file, template_file, chain_name='default_chain'):
    try:
        with open(input_file, "r") as file:
            data = json.load(file)
            if data[0]: 
                extractors = data
            else:
                extractors = data["extractors"]
                

        extractor_programs = ""
        for extractor in extractors:
            module_name = extractor["module_name"]
            module = module_name.split(".")[0]
            extractor_programs += f"""
            [program:{chain_name}-{module}]
            command=indexify-extractor join-server {module_name} --coordinator-addr localhost:8950 --ingestion-addr localhost:8900
            autostart=true
            autorestart=true
            stderr_logfile=_local_data/supervisor/logs/{chain_name}-{module}.err.log
            stdout_logfile=_local_data/supervisor/logs/{chain_name}-{module}.out.log
            priority=3
            """

        with open(template_file, "r") as file:
            template = file.read()

        supervisord_conf = template.replace("{extractor_programs}", extractor_programs.strip())

        with open(output_file, "w") as file:
            file.write(supervisord_conf)

        print(f"Generated supervisord.conf at {output_file}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")
    except IOError as e:
        print(f"Error writing to file: {e}")