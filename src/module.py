import os
import yaml
from yaml.loader import SafeLoader

from .installer import Installer
from .node import Node
from .builder import Builder


class Module(Node):
  def __init__(self, folder: str, builder: Builder) -> None:
    super().__init__()
    self.folder = str
    self.config_file = os.path.join(folder, "config.yaml")

    f = open(self.config_file)
    data = yaml.load(f, Loader=SafeLoader)
    deps = builder.dependencies(data)
    for dep in deps:
      self.add_node(dep)

  def visit(self, inst: Installer):
    super().visit(inst)


def get_all_modules(builder: Builder) -> list[Module]:
  lst: list[Module] = []
  for filename in os.listdir("."):
    package = os.path.join(".", filename)
    conf = os.path.join(package, "config.yaml")
    if os.path.isdir(package) and os.path.exists(conf):
      lst.append(Module(package, builder))
  return lst
