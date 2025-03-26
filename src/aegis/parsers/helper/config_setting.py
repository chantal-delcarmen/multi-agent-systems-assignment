from typing import override
from aegis.parsers.helper.param import Param


class ConfigSetting:
    def __init__(self, name_of_settings: str, param_list: list[Param]):
        self.name_of_settings: str = name_of_settings
        self.param_list: list[Param] = param_list

    @override
    def __str__(self) -> str:
        return (
            f"{self.name_of_settings}  = {Param.param_list_to_string(self.param_list)};"
        )

    @staticmethod
    def config_list_to_string(config_list: list["ConfigSetting"]) -> str:
        config_entries = "\n".join(f"\t{config}" for config in config_list)
        return f"Config\n{{\n{config_entries}\n}}"
