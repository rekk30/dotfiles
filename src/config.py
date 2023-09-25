import os
from enum import Enum

from .installer import Installer
from .node import Node
from .const import DOTFILES_DIR, HOME_DIR


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


class Config(Node):
  def __init__(self, config) -> None:
    super().__init__()
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
    super().visit(inst)
    if self.status != ConfigStatus.CURRENT:
      inst.install_config(self.src(), self.dst())
