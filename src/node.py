from __future__ import annotations
from enum import Enum
from abc import ABC, abstractmethod

from .installer import Installer


class NodeType(Enum):
  CONFIG = 0
  PACKAGE = 1
  SCRIPT = 2

  def __str__(self) -> None:
    strings: dict[NodeType, str] = {
        NodeType.CONFIG: "Config",
        NodeType.PACKAGE: "Package",
        NodeType.SCRIPT: "Script"
    }
    return strings[NodeType(self.value)]


class Node(ABC):
  def __init__(self) -> None:
    self.nodes: list[Node] = []

  def add_node(self, node: Node):
    self.nodes.append(node)

  @abstractmethod
  def visit(self, inst: Installer):
    for node in self.nodes:
      node.visit(inst)
