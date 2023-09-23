from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum


class Installer(ABC):
  @abstractmethod
  # TODO change package dir
  # TODO change package repository
  def installPackage(self, name: str, repository: int = 0, dir: int = 0):
    pass

  @abstractmethod
  # TODO change permission type
  def installConfig(self, src: str, dst: str, permissions: int = 777):
    pass

  @abstractmethod
  def installScript(self, file: str, sudo: bool = False) -> bool:
    pass

  @abstractmethod
  def installCommand(self, command: str, sudo: bool = False) -> bool:
    pass


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


class DefaultInstaller(Installer):  # TODO change name
  def installPackage(self, name: str, repository: int = 0, dir: int = 0):
    print(f"installing package {name}")

  # TODO change permission type
  def installConfig(self, src: str, dst: str, permissions: int = 777):
    print(f"installing config {src} -> {dst}")

  def installScript(self, file: str, sudo: bool = False) -> bool:
    print(f"installing script {file}")

  def installCommand(self, command: str, sudo: bool = False) -> bool:
    print(f"installing command {command}")
