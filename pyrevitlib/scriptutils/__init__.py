import sys
from pyrevit import EXEC_PARAMS

try:
    # noinspection PyUnresolvedReferences
    COMMAND_NAME = EXEC_PARAMS.command_name
    # noinspection PyUnresolvedReferences
    COMMAND_PATH = EXEC_PARAMS.command_path
except:
    raise Exception('This is not a pyRevit script environment. These tools are irrelevant here.')


# suppress any warning generated by native or third-party modules
import warnings
warnings.filterwarnings("ignore")


import os.path as op
from pyrevit.coreutils.logger import get_logger


scriptutils_logger = get_logger(__name__)
scriptutils_logger.debug('Executing script: {} @ {}'.format(COMMAND_NAME, COMMAND_PATH))


class PyRevitScriptUtils:
    def __init__(self):
        from pyrevit.usagelog import CommandCustomResults
        self._custom_results = CommandCustomResults()

    @property
    def info(self):
        from pyrevit.extensions.extensionmgr import get_command_from_path
        return get_command_from_path(COMMAND_PATH)

    @property
    def pyrevit_version(self):
        from pyrevit.versionmgr import PYREVIT_VERSION
        return PYREVIT_VERSION

    @property
    def ipy_engine(self):
        from pyrevit.coreutils import ipyengine
        try:
            return ipyengine.get_engine_wrapper()
        except:
            raise Exception('__engine__ not found at script runtime.')

    @property
    def output(self):
        from pyrevit.coreutils.console.output import output_window
        return output_window

    @property
    def config(self):
        from pyrevit.userconfig import user_config
        script_cfg_postfix = 'config'

        try:
            return user_config.get_section(COMMAND_NAME + script_cfg_postfix)
        except:
            return user_config.add_section(COMMAND_NAME + script_cfg_postfix)

    @staticmethod
    def exit():
        sys.exit()

    @staticmethod
    def save_config():
        from pyrevit.userconfig import user_config
        user_config.save_changes()

    @property
    def ui_button(self):
        from pyrevit.coreutils.ribbon import get_current_ui
        pyrvt_tabs = get_current_ui().get_pyrevit_tabs()
        for tab in pyrvt_tabs:
            button = tab.find_child(COMMAND_NAME)
            if button:
                return button
        return None

    @property
    def results(self):
        return self._custom_results

    @staticmethod
    def get_universal_data_file(file_id, file_ext):
        """Returns a filename to be used by a user script to store data.
        These files are not marked by host Revit version and could be shared between all Revit versions and instances.
        Data files are saved in app directory and are NOT cleaned up at Revit restart.
        Script should manage cleaning up these data files.
        """
        from pyrevit.coreutils.appdata import get_universal_data_file
        script_file_id = '{}_{}'.format(COMMAND_NAME, file_id)
        return get_universal_data_file(script_file_id, file_ext)

    @staticmethod
    def get_data_file(file_id, file_ext):
        """Returns a filename to be used by a user script to store data.
        Data files are saved in app directory and are NOT cleaned up at Revit restart.
        Script should manage cleaning up these data files.
        """
        from pyrevit.coreutils.appdata import get_data_file
        script_file_id = '{}_{}'.format(COMMAND_NAME, file_id)
        return get_data_file(script_file_id, file_ext)

    @staticmethod
    def get_instance_data_file(file_id):
        """Returns a filename to be used by a user script to store data under current Revit instance.
        Instance data files are saved in app directory and are cleaned up at Revit restart.
        """
        from pyrevit.coreutils.appdata import get_instance_data_file
        script_file_id = '{}_{}'.format(COMMAND_NAME, file_id)
        return get_instance_data_file(script_file_id)

    @property
    def instance_data_file(self):
        return self.get_instance_data_file('defaultdata')

    @staticmethod
    def get_bundle_file(file_name):
        return op.join(COMMAND_PATH, file_name)

    @staticmethod
    def journal_write(data_key, msg):
        # Get the StringStringMap class which can write data into.
        # noinspection PyUnresolvedReferences
        data_map = __commandData__.JournalData
        data_map.Clear()

        # Begin to add the support data
        data_map.Add(data_key, msg)

    @staticmethod
    def journal_read(data_key):
        # Get the StringStringMap class which can write data into.
        # noinspection PyUnresolvedReferences
        data_map = __commandData__.JournalData

        # Begin to get the support data
        return data_map[data_key]

# ----------------------------------------------------------------------------------------------------------------------
# Utilities available to scripts
# ----------------------------------------------------------------------------------------------------------------------
# noinspection PyUnresolvedReferences
import pyrevit.coreutils as coreutils
# noinspection PyUnresolvedReferences
from pyrevit.coreutils import show_file_in_explorer, open_url
# noinspection PyUnresolvedReferences
from pyrevit.coreutils.envvars import get_pyrevit_env_var, set_pyrevit_env_var


# logger for this script
logger = get_logger(COMMAND_NAME)
# setup this script services
this_script = PyRevitScriptUtils()


def print_md(md_str):
    logger.warning('print_md is deprecated and will be removed soon. Please use this_script.output.print_md')
    this_script.output.print_md(md_str)


def print_code(code_str):
    logger.warning('print_code is deprecated and will be removed soon. Please use this_script.output.print_code')
    this_script.output.print_code(code_str)
