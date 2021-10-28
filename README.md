# Adam RMS Crud Generator

This a generator to take a set of entity files in nest-js and creates nest js controllers and services for them. 
This has been written for the [Adam RMS](https://github.com/bstudios/adam-rms) project.

# Usage
First install the requirements by running `pip install -r requirements.txt`

You can then run `python generator.py /path/to/adamRMS/api/src` and it will generate the CRUD routes for all entities 
in the project.

Alternatively you can run `python generator.py /path/to/adamRMS/api/src/{entityName}.entity.ts` replacing entityName with
an entity. This will generate the CRUD routes for just that entity.

