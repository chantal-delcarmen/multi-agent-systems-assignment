from typing import override

from aegis.common.commands.aegis_command import AegisCommand


class PREDICT_RESULT(AegisCommand):
    """
    Represents the result of an agent's prediction.

    Attributes:
        surv_id (int): The id of the survivor (predictions are based on saved survivors, so this is the id of the survivor associated with the prediction).
        prediction_correct (bool): If the agent's prediction was correct or not.
    """

    def __init__(self, surv_id: int, prediction_correct: bool) -> None:
        """
        Initializes a PREDICT_RESULT instance.

        Args:
            surv_id: The id of the survivor (predictions are based on saved survivors, so this is the id of the survivor associated with the prediction).
            prediction_correct: If the agent's prediction was correct or not.
        """
        self.surv_id = surv_id
        self.prediction_correct = prediction_correct

    @override
    def __str__(self) -> str:
        return f"{self.STR_PREDICT_RESULT} ( SURV_ID {self.surv_id} , PREDICTION_CORRECT {self.prediction_correct} )"
