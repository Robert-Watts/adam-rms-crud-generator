import argparse
import os

def get_arguments() -> str:
    """
    Gets the CLI arguments and returns them

    :return: A string with a path to a folder or file
    """
    parser = argparse.ArgumentParser(description='Write services and controllers for a adam-rms entity.')
    parser.add_argument('path', type=str, help='The path of a entity or root directory')
    args = parser.parse_args()
    return args.path

def get_all_entities(path: str) -> [str]:
    """
    Takes the string, checks if its a file or a folder. If its a folder it
    recursively gets all files that end with entity.ts

    :param path: The path to look up - str
    :return: An array of strings
    """
    if(os.path.isfile(path)):
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
    return os.path.dirname(path),os.path.basename(path).split(".")[0]

def write_service(entity_path: str, entity_name: str):
    pass

def write_controller(entity_path, entity_name: str):
    pass

def main():
    path = get_arguments()
    entities = get_all_entities(path)
    for entity_path in entities:
        entity_name, entity_folder = get_entity_name_and_folder(entity_path)
        print("Writing CRUD for %s in %s" % (entity_name, entity_folder))
        write_service(entity_folder, entity_name)
        write_controller(entity_folder, entity_name)

if __name__ == '__main__':
    main()
