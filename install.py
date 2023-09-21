#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import sys
import os
import logging as log
import filecmp
import argparse
import subprocess
import getpass

import yaml
from yaml.loader import SafeLoader

from src.module import get_all_modules
from src.installer import DefaultInstaller


def check_user_pass(password: str) -> bool:
  process = subprocess.Popen(
      "sudo -S true", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
  process.communicate(password)
  return process.wait() == 0


def exit_sudo():
  process = subprocess.Popen(
      "sudo -k", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
  process.wait()


def get_user_pass():
  global USER_PASSWORD  # TODO probably a terrible thing
  USER_PASSWORD = getpass.getpass("Enter user password: ")
  if not check_user_pass(USER_PASSWORD):
    log.error('Wrong password', stack_info=True)
    os._exit(1)
  exit_sudo()


def enter_sudo():
  # TODO do I need this
  process = subprocess.Popen(
      "sudo -S true", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
  process.communicate(USER_PASSWORD)
  ret = process.wait()
  if ret != 0:
    log.error("Failed to enter sudo", stack_info=True)
    os._exit(1)


def main(args):
  log.basicConfig()
  # log.getLogger().setLevel(log.DEBUG)
  # log.info(f"Dotfiles folder: {DOTFILES_DIR}")
  # log.info(f"Home folder: {HOME_DIR}")

  print(f"Current user: {os.getenv('USER')}")
  get_user_pass()

  parser = argparse.ArgumentParser()

  parser.add_argument("-d", "--dry", action="store_true")

  args = parser.parse_args()

  updated: bool = False

  modules = get_all_modules()
  installer = DefaultInstaller()

  for module in modules:
    module.visit(installer)

  # for module in modules:
  #   module_change: bool = False
  #   for file in module.files():
  #     if file.status == ConfigStatus.OBSOLETE:
  #       print(f'{file.dst()} -> {str(file.status)}')
  #       module_change = True
  #       updated = True
  #       if not args.dry:
  #         file.create_symlink()

  #   if module_change and not args.dry:
  #     for command in module.scripts():
  #       command.execute()

  # if not updated:
  #   print("Everything up to date")


if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
