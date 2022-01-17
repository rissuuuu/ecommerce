from pathlib import Path
from alembic.config import Config
from alembic import command
from main import app
import glob
import user_components
import alert_components

settings = app.ctx.settings


class AlembicCommand:
    alembic_paths = []
    def __init__(self):
        self.alembic_paths.extend(
            glob.glob(f"{str(Path(user_components.__file__).parent)}/**/alembic.ini")
        )
        self.alembic_paths.extend(
            glob.glob(f"{str(Path(alert_components.__file__).parent)}/**/alembic.ini")
        )
        self.alembic_configs = []
        for path in self.alembic_paths:
            alembic_cfg = Config(path)
            alembic_cfg.set_main_option("sqlalchemy.url", settings.pg_dsn)
            alembic_cfg.set_main_option(
                "script_location", str(Path(path).parent.joinpath("alembic"))
            )
            self.alembic_configs.append(alembic_cfg)

    def current(self) -> None:
        """show current revision"""
        for config in self.alembic_configs:
            command.current(config)

    def heads(self):
        """show available heads"""
        for config in self.alembic_configs:
            command.heads(config)

    def history(self):
        """show revision history"""
        for config in self.alembic_configs:
            command.history(config)

    def migrate(self, revision: str = "head", sql=False) -> None:
        """upgrade to a revision"""
        for config in self.alembic_configs:
            command.upgrade(config, revision=revision, sql=sql)

    def rollback(self, revision: str) -> None:
        """downgrade revision"""
        for config in self.alembic_configs:
            command.downgrade(config, revision=revision)

    def branches(self, verbose: bool = False) -> None:
        """list all branches"""
        for config in self.alembic_configs:
            command.branches(config, verbose=verbose)

    def show(self, rev: str) -> None:
        """show revision info"""
        for config in self.alembic_configs:
            command.show(config, rev=rev)


a = AlembicCommand()
a.migrate()
a.current()
a.heads()
a.history()
