"""Defines the TOML finopspp config file"""
from pydantic import Field

from finopspp.models.core import Config


class Framework(Config):
    """Model for the basic section of the variables config"""
    project_path: str = Field(
        description='Local path to the FinOps++ Framework-Assessment project'
    )


class Configuration(Config):
    """Model specification for the variables config"""
    framework: Framework
