import os
import random

import numpy as np
from numpy.typing import NDArray

from aegis.common import AgentID
from aegis.common.constants import Constants


class PredictionHandler:
    # (gid, survivor_id), ([agent(s) helped save], idx for img/label)
    _no_pred_yet: dict[tuple[int, int], tuple[list[AgentID], int]] = {}

    # gid, {survivor_id: (agent_id, prediction_correct)}
    _pred_results: dict[int, dict[int, tuple[int, bool]]] = {}

    aegis_testing_output_dir = os.path.join(
        "src", "aegis", "agent_predictions", "model_testing_data"
    )
    _x_test: NDArray[np.float32] = np.load(
        os.path.join(aegis_testing_output_dir, "x_test_a3.npy")
    )
    _y_test: NDArray[np.int64] = np.load(
        os.path.join(aegis_testing_output_dir, "y_test_a3.npy")
    )
    _unique_labels: NDArray[np.int64] = np.unique(_y_test)

    @staticmethod
    def initialize_testing_data() -> None:
        pass
        # if PredictionHandler._x_test is None or PredictionHandler._y_test is None:
        #     PredictionHandler._x_test = np.load(os.path.join(aegis_testing_output_dir, "x_test.npy"))
        #     PredictionHandler._y_test = np.load(os.path.join(aegis_testing_output_dir, "y_test.npy"))

    @staticmethod
    def get_image_from_index(index: int) -> NDArray[np.float32]:
        # print(f"\n\nx_test shape: {PredictionHandler._x_test.shape}\n\n\n")
        return PredictionHandler._x_test[index]

    @staticmethod
    def get_label_from_index(index: int) -> int:
        # print(f"\n\ny_test shape: {PredictionHandler._y_test.shape}\n\n\n")
        return PredictionHandler._y_test[index]

    @staticmethod
    def is_group_in_no_pred_yet(gid: int, survivor_id: int) -> bool:
        return (gid, survivor_id) in PredictionHandler._no_pred_yet

    @staticmethod
    def is_agent_in_saving_group(agent_id: AgentID, survivor_id: int) -> bool:
        gid = agent_id.gid
        key = (gid, survivor_id)
        if key in PredictionHandler._no_pred_yet:
            agents_helped_save, _ = PredictionHandler._no_pred_yet[key]
            return agent_id in agents_helped_save
        return False

    @staticmethod
    def add_agent_to_no_pred_yet(agent_id: AgentID, survivor_id: int) -> None:
        gid = agent_id.gid
        key = (gid, survivor_id)
        if key in PredictionHandler._no_pred_yet:
            agents_helped_save, _ = PredictionHandler._no_pred_yet[key]
            agents_helped_save.append(agent_id)
        else:
            agents_helped_save = [agent_id]
            random_index = random.randint(0, Constants.NUM_OF_TESTING_IMAGES - 1)
            PredictionHandler._no_pred_yet[key] = (agents_helped_save, random_index)

    @staticmethod
    def _remove_group_surv_from_no_pred_yet(gid: int, survivor_id: int) -> None:
        key = (gid, survivor_id)
        if key in PredictionHandler._no_pred_yet:
            del PredictionHandler._no_pred_yet[key]

    @staticmethod
    def get_pred_info_for_agent(
        agent_id: AgentID,
    ) -> tuple[int, NDArray[np.float32], NDArray[np.int64]] | None:
        # find agent in a list of agent(s) helped saved and return pred_info for it, otherwise return None
        for (gid, surv_id), (
            agents_helped_save,
            idx,
        ) in PredictionHandler._no_pred_yet.items():
            # filter to check only entries with agents group
            if agent_id.gid == gid:
                if agent_id in agents_helped_save:
                    return (
                        surv_id,
                        PredictionHandler._x_test[idx],
                        PredictionHandler._unique_labels,
                    )
        return None

    @staticmethod
    def check_agent_prediction(
        agent_id: AgentID, survivor_id: int, label: np.int64
    ) -> bool:
        gid = agent_id.gid
        key = (gid, survivor_id)
        if key in PredictionHandler._no_pred_yet:
            _, idx = PredictionHandler._no_pred_yet[key]
            return PredictionHandler._y_test[idx] == label
        return False

    @staticmethod
    def set_prediction_result(
        agent_id: AgentID, survivor_id: int, prediction_correct: bool
    ) -> None:
        gid = agent_id.gid
        if gid not in PredictionHandler._pred_results:
            PredictionHandler._pred_results[gid] = {}
        PredictionHandler._pred_results[gid][survivor_id] = (
            agent_id.id,
            prediction_correct,
        )

        # remove this group and the surv from no_pred_yet, since this agent made the prediction for the group, and only one person from a group needs to make a prediction
        PredictionHandler._remove_group_surv_from_no_pred_yet(agent_id.gid, survivor_id)

    @staticmethod
    def get_prediction_result(agent_id: AgentID) -> tuple[int, bool] | None:
        if agent_id.gid in PredictionHandler._pred_results:
            for surv_id, (
                agent_id_responsible,
                prediction_correct,
            ) in PredictionHandler._pred_results[agent_id.gid].items():
                if agent_id_responsible == agent_id.id:
                    return surv_id, prediction_correct
        return None
