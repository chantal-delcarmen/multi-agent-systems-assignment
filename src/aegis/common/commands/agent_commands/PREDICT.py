from typing import override

import numpy as np

from aegis.common.commands.agent_command import AgentCommand


class PREDICT(AgentCommand):
    """
    Represents the prediction of an agent.

    Attributes:
        surv_id (int): The id of the survivor (predictions are based on saved survivors, so this is the id of the survivor associated with the prediction).
        label (np.int64): The label of the prediction.
    """

    def __init__(self, surv_id: int, label: np.int64):
        """
        Initializes a PREDICT instance.

        Args:
            surv_id: The id of the survivor (predictions are based on saved survivors, so this is the id of the survivor associated with the prediction).
            label: The label of the prediction.
        """
        super().__init__()
        self.surv_id = surv_id
        self.label = label

    @override
    def __str__(self) -> str:
        return f"{self.STR_PREDICT} ( SURV_ID {self.surv_id} , LABEL {self.label} )"

    @override
    def proc_string(self) -> str:
        return f"{self._agent_id.proc_string()}#Prediction {self.label} for survivor {self.surv_id}"
