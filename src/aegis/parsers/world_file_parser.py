import json
from typing import cast

from aegis.common import AgentID, InternalLocation
from aegis.parsers.aegis_world_file import AegisWorldFile
from aegis.parsers.helper.cell_info_settings import CellInfoSettings
from aegis.parsers.helper.cell_type_info import CellTypeInfo
from aegis.parsers.helper.world_file_type import (
    AgentInfo,
    CellLoc,
    CellTypes,
    SpawnInfo,
    StackInfo,
    WorldFileType,
)
from aegis.world.spawn_manager import SpawnZone, SpawnZoneType


class WorldFileParser:
    @staticmethod
    def parse_world_file(filename: str) -> AegisWorldFile | None:
        try:
            with open(filename, "r") as file:
                data: WorldFileType = json.load(file)
                width = data["settings"]["world_info"]["size"]["width"]
                height = data["settings"]["world_info"]["size"]["height"]
                agent_energy = data["settings"]["world_info"]["agent_energy"]
                seed = data["settings"]["world_info"]["seed"]
                high_survivor_level = data["settings"]["world_info"][
                    "world_file_levels"
                ]["high"]

                mid_survivor_level = data["settings"]["world_info"][
                    "world_file_levels"
                ]["mid"]
                low_survivor_level = data["settings"]["world_info"][
                    "world_file_levels"
                ]["low"]

                cell_settings = WorldFileParser._parse_cell_settings(data["cell_types"])
                cell_stack_info = WorldFileParser._parse_cell_stack_info(data["stacks"])
                agent_spawn_locations = WorldFileParser._parse_spawn_locations(
                    data["spawn_locs"]
                )
                return AegisWorldFile(
                    width,
                    height,
                    agent_energy,
                    seed,
                    high_survivor_level,
                    mid_survivor_level,
                    low_survivor_level,
                    cell_stack_info,
                    cell_settings,
                    agent_spawn_locations,
                )
        except Exception as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def _parse_cell_stack_info(
        cell_stack_info: list[StackInfo],
    ) -> list[CellInfoSettings]:
        return [
            CellInfoSettings(
                cell["move_cost"],
                cell["contents"],
                InternalLocation(cell["cell_loc"]["x"], cell["cell_loc"]["y"]),
            )
            for cell in cell_stack_info
        ]

    @staticmethod
    def _parse_cell_settings(cell_types: CellTypes) -> list[CellTypeInfo]:
        return [
            CellTypeInfo(
                name,
                [
                    InternalLocation(loc["x"], loc["y"])
                    for loc in cast(list[CellLoc], cell_locs)
                ],
            )
            for name, cell_locs in cell_types.items()
        ]

    @staticmethod
    def _parse_agents(agents: list[AgentInfo]) -> dict[AgentID, InternalLocation]:
        return {
            AgentID(agent_info["id"], agent_info["gid"]): InternalLocation(
                agent_info["x"], agent_info["y"]
            )
            for agent_info in agents
        }

    @staticmethod
    def _parse_spawn_locations(
        spawn_locs: list[SpawnInfo],
    ) -> list[SpawnZone]:
        spawns: list[SpawnZone] = []

        for loc in spawn_locs:
            zone_type = SpawnZoneType(loc["type"])
            location = InternalLocation(loc["x"], loc["y"])
            gid = loc.get("gid")
            spawn = SpawnZone(location, zone_type, gid)
            spawns.append(spawn)

        return spawns
