from abc import ABC, abstractmethod
from installer import Node, Installer
from module import get_nodes


class Procedure(Node):
  @abstractmethod
  def visit(self, inst: Installer):
    pass
  # def execute(self) -> int:
  #   raise NotImplementedError("Subclass must implement this method")


def make_procedure(config) -> Procedure:
  if "command" in config:
    return Command(config)
  raise f"Incorrect command configuration\n{config}"


class Command(Procedure):
  def __init__(self, config) -> None:
    super().__init__()
    self.__command = config["command"]
    self.strict = False
    self.sudo = False
    self.nodes = get_nodes()

    if "strict" in config:
      self.strict = config["strict"]

    if "sudo" in config:
      self.sudo = config["sudo"]

  # def execute(self) -> int:
  #   log.debug(f"Execute command: \"{self.__command}\"")
  #   if self.sudo:
  #     log.info("Entering sudo...")
  #     enter_sudo()

  #   process = subprocess.Popen(
  #       self.__command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  #   ret = process.wait()
  #   if ret != 0:
  #     err = process.communicate()[1]
  #     log.debug(f"Command failed:\n{err}")
  #   else:
  #     out = process.communicate()[0]
  #     log.debug(f"Command output:\n{out}")

  #   if self.sudo:
  #     exit_sudo()
  #   return ret
