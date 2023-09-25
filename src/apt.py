import subprocess
import logging as log
from .installer import PackageInstaller, PackageChecker


class Apt(PackageInstaller, PackageChecker):  # TODO different repo
  def install_package(self, name: str, repository: int = 0, dir: int = 0):
    process = subprocess.Popen(
        f"sudo apt install {name}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    ret = process.wait()
    if ret != 0:
      err = process.communicate()[1]
      log.debug(f"Command failed:\n{err}")
    else:
      out = process.communicate()[0]
      log.debug(f"Command output:\n{out}")

  def is_installed(self, name: str) -> bool:
    process = subprocess.Popen(
        f"dpkg -s {name}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    ret = process.wait()
    return ret == 0
