from .node import Node, NodeType
from .config import Config
from .package import Package
from .scripts import make_procedure, Procedure


class Builder:
  def dependencies(self, yaml) -> list[Node]:
    nodes: list[Node] = []
    if "scripts" in yaml:
      for val in yaml["scripts"]:
        nodes.append(self.build(val, NodeType.SCRIPT))
      del yaml["scripts"]

    if "files" in yaml:
      for val in yaml["files"]:
        nodes.append(self.build(val, NodeType.CONFIG))
      del yaml["files"]

    if "packages" in yaml:
      for val in yaml["packages"]:
        nodes.append(self.build(val, NodeType.PACKAGE))
      del yaml["packages"]

    return nodes

  def build(self, yaml, node_type: NodeType) -> Node:
    node: Node
    dependencies: list[Node] = self.dependencies(yaml)

    match node_type:
      case NodeType.CONFIG:
        node = Config(yaml)
      case NodeType.PACKAGE:
        node = Package(yaml)
      case NodeType.SCRIPT:
        node = make_procedure(yaml)
      case _:
        raise Exception("Wrong node type")

    for dep in dependencies:
      node.add_node(dep)
    return node
