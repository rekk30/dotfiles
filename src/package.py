from .installer import Node, Installer


class Package(Node):
  def __init__(self, config) -> None:
    super().__init__()
    self.name = ""
    self.pmg = 0  # TODO package managers enum

    if "apt" in config:
      self.name = config["apt"]

  def visit(self, inst: Installer):
    super().visit(inst)
    inst.installPackage(self.name)
