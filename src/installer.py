from abc import ABC, abstractmethod


class PackageIntaller(ABC):
  @abstractmethod
  # TODO change package dir
  # TODO change package repository
  def installPackage(self, name: str, repository: int = 0, dir: int = 0):
    pass


class ConfigIntaller(ABC):
  @abstractmethod
  # TODO change permission type
  def installConfig(self, src: str, dst: str, permissions: int = 777):
    pass


class ScriptInstaller(ABC):
  @abstractmethod
  def installScript(self, file: str, sudo: bool = False) -> bool:
    pass


class CommandInstaller(ABC):
  @abstractmethod
  def installCommand(self, command: str, sudo: bool = False) -> bool:
    pass


class Installer(PackageIntaller, ConfigIntaller, ScriptInstaller, CommandInstaller):
  pass
