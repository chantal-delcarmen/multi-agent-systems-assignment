from enum import Enum
import random

from aegis.common.location import InternalLocation


class SpawnZoneType(Enum):
    GROUP = "group"
    ANY = "any"


class SpawnZone:
    def __init__(
        self,
        location: InternalLocation,
        zone_type: SpawnZoneType,
        allowed_group: int | None = None,
    ) -> None:
        self.location: InternalLocation = location
        self.zone_type: SpawnZoneType = zone_type
        self.allowed_group: int | None = allowed_group
        self.spawned: bool = False

    def can_spawn(self, group_id: int | None) -> bool:
        if self.spawned:
            return False
        if self.zone_type == SpawnZoneType.ANY:
            return True
        return group_id == self.allowed_group

    def set_spawned(self) -> None:
        self.spawned = True


class SpawnManger:
    def __init__(self) -> None:
        self.spawn_locations: list[SpawnZone] = []

    def add_spawn_zone(self, spawn: SpawnZone) -> None:
        if spawn.zone_type == SpawnZoneType.GROUP and spawn.allowed_group is None:
            raise ValueError("Group spawn zones require a group id!")

        self.spawn_locations.append(spawn)

    def get_spawn_location(self, group_id: int | None) -> InternalLocation:
        # Prio group zones first

        group_spawns = [
            spawn
            for spawn in self.spawn_locations
            if spawn.zone_type == SpawnZoneType.GROUP and spawn.can_spawn(group_id)
        ]

        if group_spawns:
            spawn = random.choice(group_spawns)
            spawn.set_spawned()
            return spawn.location

        any_spawns = [
            spawn
            for spawn in self.spawn_locations
            if spawn.zone_type == SpawnZoneType.ANY and spawn.can_spawn(group_id)
        ]

        return random.choice(any_spawns).location
