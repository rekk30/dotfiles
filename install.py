#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import sys
import os
import logging as log
import filecmp
import shutil
import argparse
import subprocess
from enum import Enum

import yaml
from yaml.loader import SafeLoader

DOTFILES_DIR: str = os.path.dirname(os.path.abspath(sys.argv[0]))
HOME_DIR: str = os.path.expanduser("~")
BACKUP_DIR: str = DOTFILES_DIR + "/backup"


def deep_file_copy(src: str, dst: str) -> None:
  if not os.path.exists(src):
    raise Exception(f"File does not exist: {src}")

  dest_dir: str = os.path.dirname(dst)
  if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

  shutil.copy(src, dst)


class FilePairStatus(Enum):
  CURRENT = 0
  OBSOLETE = 1
  MISSING = 2

  def __str__(self) -> None:
    strings: dict[FilePairStatus, str] = {
        FilePairStatus.CURRENT: "Up to date",
        FilePairStatus.OBSOLETE: "Obsolete",
        FilePairStatus.MISSING: "Source file missing"
    }
    return strings[FilePairStatus(self.value)]


class FilePair:
  def __init__(self, src: str, dst: str) -> None:
    self.__src: str = src
    self.__dst: str = dst
    self.status: FilePairStatus = FilePairStatus.OBSOLETE

    if not os.path.exists(self.src()):
      self.status = FilePairStatus.MISSING
      return

    if os.path.islink(self.dst()) and os.readlink(self.dst()) == self.src():
      self.status = FilePairStatus.CURRENT

  def src(self) -> str:
    return DOTFILES_DIR + "/" + self.__src

  def dst(self) -> str:
    return HOME_DIR + "/" + self.__dst

  def create_symlink(self) -> None:
    log.info(f"Symlink {self.src()} -> {self.dst()}")

    exist: bool = os.path.exists(self.dst())

    if exist:
      backup_file: str = BACKUP_DIR + "/" + self.__src
      deep_file_copy(self.dst(), backup_file)
      os.remove(self.dst())
      log.warning(f"Old file has been backed up: {backup_file}")

    os.symlink(self.src(), self.dst())


class Procedure:
  def execute(self) -> int:
    raise NotImplementedError("Subclass must implement this method")


def make_procedure(config) -> Procedure:
  if "command" in config:
    return Command(config)
  raise f"Incorrect command configuration\n{config}"


class Command(Procedure):
  def __init__(self, config) -> None:
    super().__init__()
    self.__command = config["command"]
    self.strict = False
    self.sudo = False

    if "strict" in config:
      self.strict = config["strict"]

    if "sudo" in config:
      self.strict = config["sudo"]

  def execute(self) -> int:
    log.debug(f"Execute command: \"{self.__command}\"")
    process = subprocess.Popen(
        self.__command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    ret = process.wait()
    if ret != 0:
      err = process.communicate()[1]
      log.debug(f"Command failed:\n{err}")
    return ret


class Module:
  def __init__(self, folder: str) -> None:
    self.folder = str
    self.config_file = os.path.join(folder, "config.yaml")

    f = open(self.config_file)
    self.data = yaml.load(f, Loader=SafeLoader)

  def files(self) -> list[FilePair]:
    return [FilePair(val["src"], val["dst"]) for val in self.data["files"]]

  def scripts(self) -> list[Procedure]:
    return [make_procedure(val) for val in self.data["scripts"]]


def get_all_modules() -> list[Module]:
  lst: list[Module] = []
  for filename in os.listdir("."):
    package = os.path.join(".", filename)
    conf = os.path.join(package, "config.yaml")
    if os.path.isdir(package) and os.path.exists(conf):
      lst.append(Module(package))
  return lst


def main(args):
  log.basicConfig()
  log.getLogger().setLevel(log.DEBUG)
  log.info(f"Dotfiles folder: {DOTFILES_DIR}")
  log.info(f"Home folder: {HOME_DIR}")

  parser = argparse.ArgumentParser()

  parser.add_argument("-d", "--dry", action="store_true")

  args = parser.parse_args()

  updated: bool = False

  modules = get_all_modules()

  for module in modules:
    module_change: bool = False
    for file in module.files():
      if file.status == FilePairStatus.OBSOLETE:
        print(f'{file.dst()} -> {str(file.status)}')
        module_change = True
        updated = True
        if not args.dry:
          file.create_symlink()

    if module_change and not args.dry:
      for command in module.scripts():
        command.execute()

  if not updated:
    print("Everything up to date")


if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
