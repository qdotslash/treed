import yaml


def load_config(yaml_config_file_location='resources/config.yaml'):
    try:
        from yaml import CLoader as Loader, CDumper as Dumper
    except ImportError:
        from yaml import Loader, Dumper

    try:
        with open(yaml_config_file_location, 'r') as yaml_in:
            config = yaml.load(yaml_in, Loader=Loader)
    except yaml.YAMLError as exc:
        if hasattr(exc, 'problem_mark'):
            mark = exc.problem_mark
            print("Error position: (%s:%s)" % (mark.line+1, mark.column+1))
            print('\nExiting in setup load yaml.')
            sys.exit()
        else:
            print("Error in configuration file:", exc)
            print('\nExiting in setup load yaml.')
            sys.exit()

    return config
