import os
import yaml
from yaml.loader import SafeLoader

from .config import Config
from .scripts import Procedure, make_procedure
from .installer import Node, Installer
from .package import Package


def get_nodes(yaml) -> list[Node]:
  nodes: list[Node] = []
  if "scripts" in yaml:
    nodes.extend([make_procedure(val) for val in yaml["scripts"]])
  if "packages" in yaml:
    nodes.extend([Package(val) for val in yaml["packages"]])
  if "files" in yaml:
    nodes.extend([Config(val) for val in yaml["packages"]])

  return nodes


class Module:
  def __init__(self, folder: str) -> None:
    self.folder = str
    self.config_file = os.path.join(folder, "config.yaml")

    f = open(self.config_file)
    data = yaml.load(f, Loader=SafeLoader)
    self.nodes = get_nodes(data)

  def visit(self, inst: Installer):
    for node in self.nodes:
      node.visit(inst)
    inst.installCommand(self.__command, self.sudo)

  # def files(self) -> list[Config]:
  #   return [Config(val["src"], val["dst"]) for val in self.data["files"]]

  # def scripts(self) -> list[Procedure]:
  #   return [make_procedure(val) for val in self.data["scripts"]]


def get_all_modules() -> list[Module]:
  lst: list[Module] = []
  for filename in os.listdir("."):
    package = os.path.join(".", filename)
    conf = os.path.join(package, "config.yaml")
    if os.path.isdir(package) and os.path.exists(conf):
      lst.append(Module(package))
  return lst
