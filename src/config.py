import os
import sys
import logging as log
from enum import Enum
import shutil

from .installer import Installer
from .module import get_nodes

DOTFILES_DIR: str = os.path.dirname(os.path.abspath(sys.argv[0]))
HOME_DIR: str = os.path.expanduser("~")
BACKUP_DIR: str = DOTFILES_DIR + "/backup"


def deep_file_copy(src: str, dst: str) -> None:
  if not os.path.exists(src):
    raise Exception(f"File does not exist: {src}")

  dest_dir: str = os.path.dirname(dst)
  if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

  shutil.copy(src, dst)


class ConfigStatus(Enum):
  CURRENT = 0
  OBSOLETE = 1
  MISSING = 2

  def __str__(self) -> None:
    strings: dict[ConfigStatus, str] = {
        ConfigStatus.CURRENT: "Up to date",
        ConfigStatus.OBSOLETE: "Obsolete",
        ConfigStatus.MISSING: "Source file missing"
    }
    return strings[ConfigStatus(self.value)]


class Config:
  def __init__(self, config) -> None:
    self.__src: str = config["src"]
    self.__dst: str = config["dst"]
    self.status: ConfigStatus = ConfigStatus.OBSOLETE

    if not os.path.exists(self.src()):
      self.status = ConfigStatus.MISSING
      return

    if os.path.islink(self.dst()) and os.readlink(self.dst()) == self.src():
      self.status = ConfigStatus.CURRENT

  def src(self) -> str:
    return DOTFILES_DIR + "/" + self.__src

  def dst(self) -> str:
    return HOME_DIR + "/" + self.__dst

  def visit(self, inst: Installer):
    for node in self.nodes:
      node.visit(inst)
    inst.installConfig(self.src(), self.dst())

  # def create_symlink(self) -> None:
  #   log.info(f"Symlink {self.src()} -> {self.dst()}")

  #   exist: bool = os.path.exists(self.dst())

  #   if exist:
  #     backup_file: str = BACKUP_DIR + "/" + self.__src
  #     deep_file_copy(self.dst(), backup_file)
  #     os.remove(self.dst())
  #     log.warning(f"Old file has been backed up: {backup_file}")

    # os.symlink(self.src(), self.dst())
