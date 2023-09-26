import os
import sys
import shutil
import subprocess
import logging as log

from .installer import ConfigInstaller, CommandInstaller, ScriptInstaller
from .const import BACKUP_DIR


def deep_file_copy(src: str, dst: str) -> None:
  if not os.path.exists(src):
    raise Exception(f"File does not exist: {src}")

  dest_dir: str = os.path.dirname(dst)
  if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

  shutil.copy(src, dst)


class UbuntuInstaller(ConfigInstaller, CommandInstaller, ScriptInstaller):
  def install_config(self, src: str, dst: str, permissions: int = 777):
    print(f"src: {src}, dst: {dst}")
    log.info(f"Symlink {src} -> {dst}")

    exist: bool = os.path.exists(dst)

    if exist:
      backup_file: str = BACKUP_DIR + "/" + src
      deep_file_copy(dst, backup_file)
      os.remove(dst)
      log.warning(f"Old file has been backed up: {backup_file}")

    os.symlink(src, dst)

  def install_script(self, file: str, sudo: bool = False) -> bool:
    raise NotImplementedError

  def install_command(self, command: str, sudo: bool = False) -> bool:
    log.debug(f"Execute command: \"{command}\"")
    if sudo:
      log.info("Entering sudo...")
      # enter_sudo()

    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    ret = process.wait()
    if ret != 0:
      err = process.communicate()[1]
      log.debug(f"Command failed:\n{err}")
    else:
      out = process.communicate()[0]
      log.debug(f"Command output:\n{out}")

    if sudo:
      # exit_sudo()
      pass
    return ret == 0
