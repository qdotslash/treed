from utils import file_utils, yaml_utils
#
#
def setup():
    try:
        config = yaml_utils.load_config()
        base_dir_dict = file_utils.return_base_dirs(config)
        return config, base_dir_dict
    except:
        return False
#
#
if __name__ == "__main__":
    main()