class Constants:
    """
    Represents the constants used throughout the game.

    Attributes:
        NORMAL_CHARGE (int): The amount of energy regained after sleeping.
        LOW_CHARGE (int): Currently not used.
        SUPER_CHARGE (int): Currently not used.
        AGENT_PORT (int): The default port used for agent and AEGIS communication.
        DEPTH_LOW_START (int): The low bound used for life signal distortion.
        DEPTH_HIGH_START (int): The upper bound used for life signal distortion.
        DEPTH_LOW_INC (int): The increment value for low distortion.
        DEPTH_HIGH_INC (int): The increment value for high distortion.
        DEFAULT_MAX_ENERGY_LEVEL (int): The max energy an agent can have.
        SAVE_STATE_ALIVE (int): The state value indicating that the survivor is alive.
        SAVE_STATE_DEAD (int): The state value indicating that the survivor is dead.
        FIRE_SPREAD (bool): Flag indicating if fire spread is enabled or not.
        WORLD_MIN (int): The minimum size of a world.
        WORLD_MAX (int): The maximum size of a world.
        NUM_OF_TESTING_IMAGES (int): The number of testing images.
    """

    NORMAL_CHARGE = 5
    LOW_CHARGE = 1
    SUPER_CHARGE = 20
    AGENT_PORT = 6001
    DEPTH_LOW_START = 0
    DEPTH_HIGH_START = 5
    DEPTH_LOW_INC = 4
    DEPTH_HIGH_INC = 5
    DEFAULT_MAX_ENERGY_LEVEL = 1000
    SAVE_STATE_ALIVE = 0
    SAVE_STATE_DEAD = 1
    FIRE_SPREAD = False
    WORLD_MIN = 3
    WORLD_MAX = 30
    SCORE_SURV_SAVED_BASE = 100
    SCORE_ANY_EXTRA_SURV_SAVED = 0
    SCORE_CORRECT_PRED = 10
    NUM_OF_TESTING_IMAGES = 704
