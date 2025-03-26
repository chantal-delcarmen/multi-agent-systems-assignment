import json
import sys
from typing import Any

from aegis.assist.config_settings import ConfigSettings
from a3.aegis_parser import AegisParser


class ConfigParser(AegisParser):
    @staticmethod
    def parse_config_file(config_file: str) -> ConfigSettings | None:
        config_settings = ConfigSettings()

        try:
            with open(config_file, "r") as file:
                data: dict[str, Any] = json.load(file)

            if "Send_Message" in data:
                send_message_data: dict[str, Any] = data["Send_Message"]

                enabled: bool = send_message_data.get("enabled", False)
                target: str = send_message_data.get("target", "ALL_GROUPS")

                config_settings.handling_messages = (
                    ConfigSettings.SEND_MESSAGES_AND_PERFORM_ACTION
                    if enabled
                    else ConfigSettings.SEND_MESSAGE_OR_PERFORM_ACTION
                )
                config_settings.send_messages_to_all_groups = (
                    ConfigSettings.SEND_MESSAGES_TO_ONLY_OWN_GROUP
                    if target == "SINGLE_GROUP"
                    else ConfigSettings.SEND_MESSAGES_TO_ALL_GROUPS
                )

            if "Sleep_On_Every" in data:
                sleep_on_every: bool = data["Sleep_On_Every"]

                config_settings.sleep_everywhere = (
                    ConfigSettings.SLEEP_ON_ALL_CELLS
                    if sleep_on_every
                    else ConfigSettings.SLEEP_ONLY_ON_CHARGING_CELLS
                )

            if "Save_Surv" in data:
                save_surv_data: dict[str, Any] = data["Save_Surv"]

                strategy: str = save_surv_data.get("strategy", "ALL")
                config_settings.points_for_saving_survivors = {
                    "ALL": ConfigSettings.POINTS_FOR_ALL_SAVING_GROUPS,
                    "RANDOM": ConfigSettings.POINTS_FOR_RANDOM_SAVING_GROUPS,
                    "COUNT": ConfigSettings.POINTS_FOR_LARGEST_SAVING_GROUPS,
                }.get(strategy, ConfigSettings.POINTS_FOR_ALL_SAVING_GROUPS)

                if strategy == "COUNT" and "tie_strategy" in save_surv_data:
                    tie_strategy: str = save_surv_data["tie_strategy"]
                    config_settings.points_for_saving_survivors_tie = {
                        "C_RANDOM": ConfigSettings.POINTS_TIE_RANDOM_SAVING_GROUPS,
                        "C_ALL": ConfigSettings.POINTS_TIE_ALL_SAVING_GROUPS,
                    }.get(tie_strategy, ConfigSettings.POINTS_TIE_ALL_SAVING_GROUPS)

            if "Predictions" in data:
                predictions_on: bool = data["Predictions"]
                config_settings.predictions_enabled = predictions_on

        except (FileNotFoundError, IOError, json.JSONDecodeError) as e:
            print(f"Aegis  : Unable to parse config file: {e}", file=sys.stderr)
            return None

        return config_settings
