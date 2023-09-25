from .installer import Installer
from .node import Node


class Package(Node):
  def __init__(self, config) -> None:
    super().__init__()
    self.name = ""
    self.pmg = 0  # TODO package managers enum

    if "apt" in config:
      self.name = config["apt"]

  def visit(self, inst: Installer):
    super().visit(inst)
    inst.install_package(self.name)
