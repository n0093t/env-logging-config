from typing import Optional, Tuple, Union

from pydantic.env_settings import (
    EnvSettingsSource,
    InitSettingsSource,
    SecretsSettingsSource,
)

from env_logging_config.spec import LoggingSettings

SettingsSources = Tuple[
    Union[
        InitSettingsSource,
        EnvSettingsSource,
        SecretsSettingsSource
    ],
    ...
]


class PrefixedConfig:
    env_prefix: str

    @classmethod
    def customise_sources(
        cls,
        init_settings: InitSettingsSource,
        env_settings: EnvSettingsSource,
        file_secret_settings: SecretsSettingsSource,
    ) -> SettingsSources:
        return env_settings, init_settings, file_secret_settings


def create_config(
    env_prefix: str,
    env_nested_delimiter: str = '.',
    defaults: Optional[dict] = None,
) -> dict:

    PrefixedConfig.env_prefix = env_prefix

    class PrefixedLoggingSettings(LoggingSettings):
        Config = PrefixedConfig

    return PrefixedLoggingSettings(
        _env_nested_delimiter=env_nested_delimiter,
        **(defaults or {})
    ).dict(exclude_none=True, by_alias=True)
