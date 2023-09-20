from installer import Node, Installer
from module import get_nodes


class Package(Node):
  def __init__(self, config) -> None:
    super().__init__()
    self.nodes: list[Node] = get_nodes(config)
    self.name = ""
    self.pmg = 0  # TODO package managers enum

    if "apt" in config:
      self.name = config["apt"]
