from msgspec import Struct
import argparse
import yaml
from pathlib import Path


class DatabaseConfig(Struct):
    user: str = "postgres"
    password: str = "postgres"
    host: str = "127.0.0.1"
    port: str = "5432"
    database_name: str = "test_db"
    url: str = None
    echo: bool = False

    def get_connection_url(self) -> str:
        if self.url:
            return self.url
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database_name}"


class KeyDBConfig(Struct):
    host: str = "127.0.0.1"
    port: str = "6379"
    db: str = "0"
    url: str = None

    def get_connection_url(self) -> str:
        if self.url:
            return self.url
        return f"keydb://{self.host}:{self.port}/{self.db}"


class JWTConfig(Struct):
    secret: str
    token_secret: str


class AppConfig(Struct):
    database: DatabaseConfig
    keydb: KeyDBConfig
    jwt: JWTConfig


def load_config(file_path: str) -> AppConfig:
    with open(file_path, "r") as f:
        config_data = yaml.safe_load(f)
    return AppConfig(
        database=DatabaseConfig(**config_data["database"]),
        keydb=KeyDBConfig(**config_data["keydb"]),
        jwt=JWTConfig(**config_data["jwt"]),
    )


def configure() -> AppConfig:
    title = "LitestarCats"
    parser = argparse.ArgumentParser(title)
    src_dir = Path(__file__).absolute().parent
    config_file = src_dir / "settings-example.yaml"
    parser.add_argument(
        "-c", "--config", type=str, default=config_file, help="Config file"
    )
    args = parser.parse_known_args()
    if args and args[0].config:
        config_file = args[0].config
    config = load_config(config_file)
    return config
