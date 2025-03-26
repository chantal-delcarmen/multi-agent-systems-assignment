from typing import override

from aegis.common import LifeSignals
from aegis.common.commands.aegis_command import AegisCommand
from aegis.common.world.info import CellInfo


class OBSERVE_RESULT(AegisCommand):
    """
    Represents the result of observing a cell.

    Attributes:
        energy_level (int): The energy_level of the agent.
        cell_info (CellInfo): The information of the cell that was observed.
        life_signals (LifeSignals): The life signals of the cell.
    """

    def __init__(
        self, energy_level: int, cell_info: CellInfo, life_signals: LifeSignals
    ) -> None:
        """
        Initializes an OBSERVE_RESULT instance.

        Args:
            energy_level: The energy_level of the agent.
            cell_info: The information of the cell that was observed.
            life_signals: The life signals of the cell.
        """
        self.energy_level = energy_level
        self.cell_info = cell_info
        self.life_signals = life_signals

    @override
    def __str__(self) -> str:
        return f"{self.STR_OBSERVE_RESULT} ( ENG_LEV {self.energy_level} , CELL_INFO ( {self.cell_info} ) , NUM_SIG {self.life_signals.size()} , LIFE_SIG {self.life_signals} )"
