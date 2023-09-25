from abc import ABC, abstractmethod
from .installer import Installer
from .node import Node


class Procedure(Node):
  @abstractmethod
  def visit(self, inst: Installer):
    pass


def make_procedure(config) -> Procedure:
  if "command" in config:
    return Command(config)
  raise f"Incorrect command configuration\n{config}"


class Command(Procedure):
  def __init__(self, config) -> None:
    super().__init__()
    self.command = config["command"]
    self.strict = False
    self.sudo = False

    if "strict" in config:
      self.strict = config["strict"]

    if "sudo" in config:
      self.sudo = config["sudo"]

  def visit(self, inst: Installer):
    super().visit(inst)
    inst.install_command(self.command, self.sudo)
