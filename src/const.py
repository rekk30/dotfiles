import os
import sys

# TODO get rid of global vars
DOTFILES_DIR: str = os.path.dirname(os.path.abspath(sys.argv[0]))
HOME_DIR: str = os.path.expanduser("~")
BACKUP_DIR: str = DOTFILES_DIR + "/backup"
