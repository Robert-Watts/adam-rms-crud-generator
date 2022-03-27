import argparse
import os
import re
from jinja2 import Environment, FileSystemLoader


def get_arguments():
    """
    Gets the CLI arguments and returns them

    :return: A string with a path to a folder or file
    """
    parser = argparse.ArgumentParser(description='Write services and controllers for a adam-rms entity.')
    parser.add_argument('path', type=str, help='The path of a entity or root directory')
    parser.add_argument('--disable_spec', action='store_true', help="Don't generate spec files")
    parser.add_argument('--disable_controller', action='store_true', help="Don't generate controller files")
    parser.add_argument('--disable_service', action='store_true', help="Don't generate service files")
    parser.add_argument('--disable_module', action='store_true', help="Don't generate a module file")

    args = parser.parse_args()
    return args


def get_all_entities(path: str) -> [str]:
    """
    Takes the string, checks if its a file or a folder. If its a folder it
    recursively gets all files that end with entity.ts

    :param path: The path to look up - str
    :return: An array of strings
    """
    if (os.path.isfile(path)):
        return [path]
    else:
        fname = []
        for root, d_names, f_names in os.walk(path):
            for f in f_names:
                if (f.endswith('entity.ts')):
                    fname.append(os.path.join(root, f))
        return fname


def get_entity_name_and_folder(path: str):
    """
    Takes the path and gets the entity name and folder
    :param path: The path to look up - str
    :return: The directory of the entity and the name (without entity.ts)
    """
    return os.path.dirname(path), os.path.basename(path).split(".")[0]


def write_service(entity_path: str, entity_name: str, jinja_env: Environment, disable_spec: bool = False):
    """
    Takes the name and path of an entity and creates a service.ts file and a service.spec.ts file for that entity.

    :param entity_path: The path of the entity
    :param entity_name: The name of the entity
    :jinja_env entity_name: The jinja Environment
    """

    def _generate_variables():
        """
        Uses the variables inherited from the parent function to generate the variables dictionary for the templates
        :return: A dictionary
        """
        return {
            "entity_name": entity_name.capitalize()
        }

    # Generate the file names and variables
    template_variables = _generate_variables()
    service_file_name = "%s.service.ts" % (entity_name)
    spec_file_name = "%s.service.spec.ts" % (entity_name)

    # Get the templates
    service_template = jinja_env.get_template('service.ts')
    spec_template = jinja_env.get_template('service.spec.ts')

    # Write the service file
    with open(os.path.join(entity_path, service_file_name), 'w') as file:
        file.write(service_template.render(template_variables))
        indent_print("Created %s" % (service_file_name))

    # Write the service spec file
    if (not disable_spec):
        with open(os.path.join(entity_path, spec_file_name), 'w') as file:
            file.write(spec_template.render(template_variables))
            indent_print("Created %s" % (spec_file_name))


def write_controller(entity_path: str, entity_name: str, jinja_env: Environment, disable_spec: bool = False):
    """
    Takes the name and path of an entity and creates a controller.ts file and a controller.spec.ts file for that entity.

    :param entity_path: The path of the entity
    :param entity_name: The name of the entity
    :jinja_env entity_name: The jinja Environment
    """

    def _generate_variables():
        """
        Uses the variables inherited from the parent function to generate the variables dictionary for the templates
        :return: A dictionary
        """
        return {
            "entity_name": entity_name.capitalize()
        }

    # Generate the file names and variables
    template_variables = _generate_variables()
    controller_file_name = "%s.controller.ts" % (entity_name)
    spec_file_name = "%s.controller.spec.ts" % (entity_name)

    # Get the templates
    controller_template = jinja_env.get_template('controller.ts')
    spec_template = jinja_env.get_template('controller.spec.ts')

    # Write the controller file
    with open(os.path.join(entity_path, controller_file_name), 'w') as file:
        file.write(controller_template.render(template_variables))
        indent_print("Created %s" % (controller_file_name))

    # Write the controller spec file
    if (not disable_spec):
        with open(os.path.join(entity_path, spec_file_name), 'w') as file:
            file.write(spec_template.render(template_variables))
            indent_print("Created %s" % (spec_file_name))

def write_module(entity_path: str, entity_name: str, file_path:str, jinja_env: Environment):
    """
    Writes a module
    :param entity_path: The path of the entity
    :param entity_name: The name of the entity
    :param file_path: The path of the entity
    :jinja_env entity_name: The jinja Environment
    """
    def _generate_variables():
        """
        Uses the variables inherited from the parent function to generate the variables dictionary for the templates
        :return: A dictionary
        """
        print(file_path)
        with open(file_path, 'r') as file:
            text = file.read()

        matches = re.findall(r'import { (.+) } from "(.+\/(.+).entity)";', text)


        clean_name = entity_name.replace("-", "")
        return {
            "entity_name": entity_name,
            "clean_entity_name": clean_name.capitalize(),
            "clean_entity_name_lower": clean_name.lower(),
            "imports":matches
        }

    # Generate the file names and variables
    template_variables = _generate_variables()
    module_file_name = "%s.module.ts" % (entity_name)

    # Get the templates
    module_template = jinja_env.get_template('module.ts')


    # Write the module file
    with open(os.path.join(entity_path, module_file_name), 'w') as file:
        file.write(module_template.render(template_variables))
        indent_print("Created %s" % (module_file_name))


def indent_print(string: str):
    """
    Output a string in the form
    :param string: A string to output "     --> %s"
    """
    print("     --> %s" % (string))


def create_jinja_env(template_folder: str = os.path.join(os.path.dirname(__file__), "templates")):
    return Environment(
        loader=FileSystemLoader(template_folder)
    )


def main():
    arguments = get_arguments()
    path = arguments.path
    entities = get_all_entities(path)

    jinja_env = create_jinja_env()

    for entity_path in entities:
        entity_folder, entity_name = get_entity_name_and_folder(entity_path)
        print("Writing CRUD for %s in %s" % (entity_name, entity_folder))

        if (not arguments.disable_service):
            write_service(entity_folder, entity_name, jinja_env, arguments.disable_spec)

        if (not arguments.disable_controller):
            write_controller(entity_folder, entity_name, jinja_env, arguments.disable_spec)

        if (not arguments.disable_module):
            write_module(entity_folder, entity_name, entity_path, jinja_env)

if __name__ == '__main__':
    main()
