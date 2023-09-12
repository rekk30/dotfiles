#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import logging as log
import filecmp
import shutil
import yaml
from yaml.loader import SafeLoader

DOTFILES_DIR: str = os.path.dirname(os.path.abspath(sys.argv[0]))
HOME_DIR: str = os.path.expanduser('~')
BACKUP_DIR: str = DOTFILES_DIR + "/backup"

def deep_file_copy(src: str, dst: str):
  if not os.path.exists(src):
    raise Exception(f'File does not exist: {src}')

  dest_dir: str = os.path.dirname(dst)
  if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

  shutil.copy(src, dst)

def create_symlink(src: str, dst: str):
  src_file: str = DOTFILES_DIR + "/" + src
  dst_file: str = HOME_DIR + "/" + dst
  log.info(f'Symlink {src_file} -> {dst_file}')

  exist: bool = os.path.exists(dst_file)

  if exist:
    if os.path.islink(dst_file) and os.readlink(dst_file) == src_file:
      log.warning(f'File has already been copied: {dst_file}')
      return
    else:
      backup_file: str = BACKUP_DIR + "/" + src
      deep_file_copy(dst_file, backup_file)
      os.remove(dst_file)
      log.warning(f'Old file has been backed up: {backup_file}')

  os.symlink(src_file, dst_file)

def main(args):
  log.basicConfig()
  log.getLogger().setLevel(log.DEBUG)
  log.info(f'Dotfiles folder: {DOTFILES_DIR}')
  log.info(f'Home folder: {HOME_DIR}')

  with open('config.yaml') as f:
    data = yaml.load(f, Loader=SafeLoader)
    # print(data["files"])
    for val in data["files"]:
      create_symlink(val["src"], val["dst"])


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))