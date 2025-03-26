from __future__ import annotations

from typing import cast, override

from aegis.common.world.objects.world_object import WorldObject
from aegis.parsers.helper.world_file_type import StackContent


class Survivor(WorldObject):
    """
    Represents a survivor layer in a cell.

    Attributes:
        id (int): The id of the survivor.
        damage_factor (int): The damage factor of the survivor.
        body_mass (int): The body mass of the survivor.
        mental_state (int): The mental state of the survivor.
    """

    def __init__(
        self,
        id: int = -1,
        energy_level: int = 1,
        damage_factor: int = 0,
        body_mass: int = 0,
        mental_state: int = 0,
    ) -> None:
        """
        Initializes a Survivor instance.

        Args:
            id: The id of the survivor.
            energy_level: The energy_level of the survivor.
            damage_factor: The damage factor of the survivor.
            body_mass: The body mass of the survivor.
            mental_state: The mental state of the survivor.
        """
        super().__init__()
        self._state = self.State.ALIVE
        self.id = id
        self.damage_factor = damage_factor
        self.body_mass = body_mass
        self.mental_state = mental_state
        self.set_energy_level(energy_level)

    def get_energy_level(self) -> int:
        """Returns the energy level of the survivor."""
        return self._energy_level

    def set_energy_level(self, energy_level: int) -> None:
        self._energy_level = energy_level
        if energy_level <= 0:
            self.set_dead()
        else:
            self.set_alive()

    def remove_energy(self, remove_energy: int) -> None:
        if remove_energy < self._energy_level:
            self._energy_level -= remove_energy
        else:
            self._energy_level = 0
            self.set_dead()

    @override
    def __str__(self) -> str:
        return f"SURVIVOR ( ID {self.id} , ENG_LEV {self._energy_level} , DMG_FAC {self.damage_factor} , BDM {self.body_mass} , MS {self.mental_state} )"

    @override
    def __repr__(self) -> str:
        return self.__str__()

    @override
    def get_name(self) -> str:
        return "Survivor"

    @override
    def get_life_signal(self) -> int:
        life_signal = self._energy_level
        if self.damage_factor > life_signal:
            return 0
        else:
            life_signal -= self.damage_factor

        if self.mental_state > life_signal:
            return 0
        else:
            life_signal -= self.mental_state

        return life_signal

    @override
    def file_output_string(self) -> str:
        return f"SV({self._energy_level},{self.damage_factor},{self.body_mass},{self.mental_state})"

    @override
    def string_information(self) -> list[str]:
        string_information = super().string_information()
        string_information.append(f"Energy Level = {self._energy_level}")
        string_information.append(f"Damage Factor = {self.damage_factor}")
        string_information.append(f"Body Mass = {self.body_mass}")
        string_information.append(f"Mental State = {self.mental_state}")
        return string_information

    @override
    def clone(self) -> Survivor:
        survivor = cast(Survivor, super().clone())
        survivor._energy_level = self._energy_level
        survivor.damage_factor = self.damage_factor
        survivor.body_mass = self.body_mass
        survivor.mental_state = self.mental_state
        return survivor

    @override
    def json(self) -> StackContent:
        return {
            "type": "sv",
            "arguments": {
                "energy_level": self._energy_level,
                "damage_factor": self.damage_factor,
                "body_mass": self.body_mass,
                "mental_state": self.mental_state,
            },
        }
