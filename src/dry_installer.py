import logging as log

from .installer import Installer
from .scripts import Command


class DryInstaller(Installer):
  def install_package(self, name: str, repository: int = 0, dir: int = 0):
    log.info(f"installing package {name}")

  def install_config(self, src: str, dst: str, permissions: int = 777):
    log.info(f"installing config {src} -> {dst}")

  def install_script(self, file: str, sudo: bool = False) -> bool:
    log.info(f"installing script {file}")

  def install_command(self, command: Command, sudo: bool = False) -> bool:
    log.info(f"installing command {command}")
