from .installer import Installer
from .installer import PackageIntaller, ConfigIntaller
from .installer import ScriptInstaller, CommandInstaller


class InstallerAnterior(Installer):
  def __init__(self, packageInst: PackageIntaller, configInst: ConfigIntaller,
               scriptInst: ScriptInstaller, commandInst: CommandInstaller) -> None:
    super().__init__()
    self.files: list[tuple[str, str]] = []
    self.commands: list[tuple[str, bool]] = []

    self.package = packageInst
    self.config = configInst
    self.script = scriptInst
    self.command = commandInst

  def installPackage(self, name: str, repository: int = 0, dir: int = 0):
    raise NotImplementedError

  def installConfig(self, src: str, dst: str, permissions: int = 777):
    self.files.append((src, dst))

  def installScript(self, file: str, sudo: bool = False) -> bool:
    raise NotImplementedError

  def installCommand(self, command: str, sudo: bool = False) -> bool:
    self.commands.append((command, sudo))

  def execute(self):
    for src, dst in self.files:
      self.config.installConfig(src, dst, 777)

    for command, sudo in self.commands:
      self.command.installCommand(command, sudo)
