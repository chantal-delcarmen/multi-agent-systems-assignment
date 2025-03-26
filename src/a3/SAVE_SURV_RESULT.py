from typing import override

import numpy as np
from numpy.typing import NDArray

from aegis.common.commands.aegis_command import AegisCommand
from aegis.common.world.info import SurroundInfo


class SAVE_SURV_RESULT(AegisCommand):
    """
    Represents the result of saving a survivor.

    Attributes:
        energy_level (int): The energy level of the agent.
        surround_info (SurroundInfo): The surrounding info of the agent.
        surv_saved_id (int): The ID of the saved survivor.
        image_to_predict (NDArray[np.float32] | None): The image to predict.
        all_unique_labels (NDArray[np.int64] | None): An array of all unique labels for prediction.
    """

    def __init__(
        self,
        energy_level: int,
        surround_info: SurroundInfo,
        pred_info: tuple[int, NDArray[np.float32], NDArray[np.int64]] | None = None,
    ) -> None:
        """
        Initializes a SAVE_SURV_RESULT instance.

        Args:
            energy_level: The energy level of the agent.
            surround_info: The surrounding info of the agent.
            pred_info: The prediction information.
        """
        self.energy_level = energy_level
        self.surround_info = surround_info
        self._pred_info = pred_info
        if pred_info:
            self.surv_saved_id = pred_info[0]
            self.image_to_predict = pred_info[1]
            self.all_unique_labels = pred_info[2]
        else:
            self.surv_saved_id = -1
            self.image_to_predict = None
            self.all_unique_labels = None

    def has_pred_info(self) -> bool:
        """
        Checks if the prediction information is available.

        Returns:
            True if prediction information is present, False otherwise.
        """
        return self._pred_info is not None

    @override
    def __str__(self) -> str:
        return f"{self.STR_SAVE_SURV_RESULT} ( ENG_LEV {self.energy_level} , SUR_INFO {self.surround_info} )"
