from abc import ABC, abstractmethod


class PackageInstaller(ABC):
  @abstractmethod
  # TODO change package dir
  # TODO change package repository
  def install_package(self, name: str, repository: int = 0, dir: int = 0):
    pass


class PackageChecker(ABC):
  @abstractmethod
  def is_installed(self, name: str) -> bool:
    pass


class ConfigInstaller(ABC):
  @abstractmethod
  # TODO change permission type
  def install_config(self, src: str, dst: str, permissions: int = 777):
    pass


class ScriptInstaller(ABC):
  @abstractmethod
  def install_script(self, file: str, sudo: bool = False) -> bool:
    pass


class CommandInstaller(ABC):
  @abstractmethod
  def install_command(self, command: str, sudo: bool = False) -> bool:
    pass


class Installer(PackageInstaller, ConfigInstaller, ScriptInstaller, CommandInstaller):
  pass
