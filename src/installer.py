from abc import ABC, abstractmethod


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


class Node(ABC):
  @abstractmethod
  def visit(self, inst: Installer):
    pass
