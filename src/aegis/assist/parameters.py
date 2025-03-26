from aegis.assist.config_settings import ConfigSettings


class Parameters:
    DEFAULT_SAVE_SURV_ENERGY_COST = 1
    DEFAULT_PREDICTION_ENERGY_COST = 1
    DEFAULT_TEAM_DIG_ENERGY_COST = 1
    DEFAULT_MOVE_ENERGY_COST = 1
    DEFAULT_OBSERVE_ENERGY_COST = 1
    milliseconds_to_wait_for_agent_command = int(1.25 * 1000)
    milliseconds_to_wait_for_agent_connect = 5 * 1000
    number_of_rounds = 500
    number_of_agents = 0
    replay_filename = "replay.txt"
    world_filename = "ExampleWorld.world"
    OBSERVE_ENERGY_COST = DEFAULT_OBSERVE_ENERGY_COST
    SAVE_SURV_ENERGY_COST = DEFAULT_SAVE_SURV_ENERGY_COST
    PREDICTION_ENERGY_COST = DEFAULT_PREDICTION_ENERGY_COST
    TEAM_DIG_ENERGY_COST = DEFAULT_TEAM_DIG_ENERGY_COST
    MOVE_ENERGY_COST = DEFAULT_MOVE_ENERGY_COST
    config_settings: ConfigSettings | None = None
