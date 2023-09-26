from .installer import Installer
from .installer import PackageInstaller, PackageChecker, ConfigInstaller
from .installer import ScriptInstaller, CommandInstaller


class InstallerAnterior(Installer):
  def __init__(self, packageInst: PackageInstaller, packageCheck: PackageChecker,
               configInst: ConfigInstaller,
               scriptInst: ScriptInstaller, commandInst: CommandInstaller) -> None:
    super().__init__()
    self.files: list[tuple[str, str]] = []
    self.commands: list[tuple[str, bool]] = []
    self.packages: list[str] = []

    self.package = packageInst
    self.package_ch = packageCheck
    self.config = configInst
    self.script = scriptInst
    self.command = commandInst

  def install_package(self, name: str, repository: int = 0, dir: int = 0):
    self.packages.append(name)

  def install_config(self, src: str, dst: str, permissions: int = 777):
    self.files.append((src, dst))

  def install_script(self, file: str, sudo: bool = False) -> bool:
    raise NotImplementedError

  def install_command(self, command: str, sudo: bool = False) -> bool:
    self.commands.append((command, sudo))

  def execute(self):
    for src, dst in self.files:
      self.config.install_config(src=src, dst=dst)
      self.config.install_config()

    for pac in self.packages:
      if not self.package_ch.is_installed(pac):
        self.package.install_command(cmd, sudo)

    for cmd, sudo in self.commands:
      self.command.install_command(cmd, sudo)
