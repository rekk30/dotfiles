import logging as log

from .installer import Installer
from .scripts import Command


class DryInstaller(Installer):
  def installPackage(self, name: str, repository: int = 0, dir: int = 0):
    log.info(f"installing package {name}")

  def installConfig(self, src: str, dst: str, permissions: int = 777):
    log.info(f"installing config {src} -> {dst}")

  def installScript(self, file: str, sudo: bool = False) -> bool:
    log.info(f"installing script {file}")

  def installCommand(self, command: Command) -> bool:
    log.info(f"installing command {command.command}")
