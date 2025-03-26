from typing import override

from aegis.common import AgentIDList, CellType, InternalLocation
from aegis.common.world.objects import WorldObject


class CellInfo:
    """
    Represents the information of a cell in the world.

    Attributes:
        cell_type (CellType): The type of the cell.
        location (InternalLocation): The location of the cell in the world.
        move_cost (int): The cost to move through the cell.
        agent_id_list (AgentIDList): A list of agent IDs on the cell.
        top_layer (WorldObject | None): Information about the top layer object.
    """

    def __init__(
        self,
        cell_type: CellType = CellType.NO_CELL,
        location: InternalLocation | None = None,
        move_cost: int = 0,
        agent_id_list: AgentIDList | None = None,
        top_layer: WorldObject | None = None,
    ) -> None:
        """
        Initializes a CellInfo instance.

        Args:
            cell_type: The type of the cell.
            location: The location of the cell.
            move_cost: The cost to move through the cell.
            agent_id_list: List of agent IDs on the cell.
            top_layer: Information about the top layer object.
        """
        self.cell_type: CellType = cell_type
        self.location: InternalLocation = (
            location if location is not None else InternalLocation(-1, -1)
        )
        self.move_cost: int = move_cost
        self.agent_id_list: AgentIDList = (
            agent_id_list if agent_id_list is not None else AgentIDList()
        )
        self.top_layer: WorldObject | None = (
            top_layer if top_layer is not None else None
        )

    @override
    def __str__(self) -> str:
        if self.cell_type == CellType.NO_CELL:
            return self.cell_type.name
        return (
            f"{self.cell_type.name} ( X {self.location.x} , Y {self.location.y} , "
            f"MV_COST {self.move_cost} , NUM_AGT {self.agent_id_list.size()} , "
            f"ID_LIST {str(self.agent_id_list)} , TOP_LAYER ( {self.top_layer} ) )"
        )
