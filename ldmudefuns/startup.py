config = None
config_file = None

def reload_config():
    """ Reloads the ldmud efuns ini configuration file.

    The file that was provided as the `config_path` to `startup()` (or
    `~/.ldmud-efuns` if no config path is provided) will be re-parsed and used
    to update the current python-efuns configuration.
    """
    if config is None or config_file is None:
        return
    global config
    config = configparser.ConfigParser()
    config['efuns'] = {}
    config.read(os.path.expanduser(config_file))


def startup(config_path='~/.ldmud-efuns'):
    """ Loads all registered packages that offer the ldmud_efun entry point.

    In the configuration file (default,`~/.ldmud-efuns`) single efuns can be
    deactivated with entries like:

        [efuns]
        name_of_the_efun = off
    """
    import pkg_resources, traceback, sys, os, configparser
    import ldmud

    global config_file
    config_file = config_path
    reload_config()
    efunconfig = config['efuns']
    print(f"Read config from {config_file}")

    for entry_point in pkg_resources.iter_entry_points('ldmud_efun'):
        if efunconfig.getboolean(entry_point.name, True):
            try:
                print(f"Registering Python efun {entry_point.name}")
                ldmud.register_efun(entry_point.name, entry_point.load())
            except:
                traceback.print_exc()
