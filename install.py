#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import sys
import os
import logging as log
import filecmp
import shutil
import argparse
from enum import Enum

import yaml
from yaml.loader import SafeLoader

DOTFILES_DIR: str = os.path.dirname(os.path.abspath(sys.argv[0]))
HOME_DIR: str = os.path.expanduser("~")
BACKUP_DIR: str = DOTFILES_DIR + "/backup"


def deep_file_copy(src: str, dst: str):
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

  def __str__(self):
    strings: dict[FilePairStatus, str] = {
        FilePairStatus.CURRENT: "Up to date",
        FilePairStatus.OBSOLETE: "Obsolete",
        FilePairStatus.MISSING: "Source file missing"
    }
    return strings[FilePairStatus(self.value)]


class FilePair:
  def __init__(self, src: str, dst: str):
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

  def create_symlink(self):
    log.info(f"Symlink {self.src()} -> {self.dst()}")

    exist: bool = os.path.exists(self.dst())

    if exist:
      backup_file: str = BACKUP_DIR + "/" + self.__src
      deep_file_copy(self.dst(), backup_file)
      os.remove(self.dst())
      log.warning(f"Old file has been backed up: {backup_file}")

    os.symlink(self.src(), self.dst())


def read_files_from_config(file: str) -> list[FilePair]:
  with open(file) as f:
    data = yaml.load(f, Loader=SafeLoader)
    return [FilePair(val["src"], val["dst"]) for val in data["files"]]


def get_all_configs() -> list[str]:
  lst: list[str] = []
  for filename in os.listdir("."):
    package = os.path.join(".", filename)
    conf = os.path.join(package, "config.yaml")
    if os.path.isdir(package) and os.path.exists(conf):
      lst.append(conf)
  return lst


def main(args):
  log.basicConfig()
  log.getLogger().setLevel(log.DEBUG)
  log.info(f"Dotfiles folder: {DOTFILES_DIR}")
  log.info(f"Home folder: {HOME_DIR}")

  parser = argparse.ArgumentParser()

  parser.add_argument("-d", "--dry", action="store_true")

  args = parser.parse_args()

  configs = get_all_configs()
  files: list[FilePair] = []

  for config in configs:
    files.extend(read_files_from_config(config))

  absolete: list[FilePair] = [
      file for file in files if file.status == FilePairStatus.OBSOLETE]

  if len(absolete) == 0:
    print("Everything up to date")

  for file in files:
    if file.status == FilePairStatus.OBSOLETE:
      print(f'{file.dst()} -> {str(file.status)}')
      if not args.dry:
        file.create_symlink()


if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
