
class Settings:

    # Screen
    WIDTH = 600
    HEIGHT = 600
    FRAME_RATE = 60
    DELTA_TIME = 1

    # Colors
    FLOOR_COLOR = (30, 0, 0)
    BULLET_COLOR_PLAYER = (255, 255, 80)
    PLAYER_COLOR = (80, 80, 255)
    ENEMY_COLOR = (255, 80, 80)

    # Bullet Attributes
    BULLET_SIZE = 2
    BULLET_SPEED = 8
    SHOOT_START_DIST = 15

    # Agent Attributes
    FOV = 120
    NUM_RAYS = 20
    FOV_RANGE = 250
    AWARENESS_RANGE = 150
    ARCHITECTURE =  [(42, ''), (23, 'relu'), (23, 'relu'), (5, 'softmax')]
    LR = 0.0008
    GAMMA = 0.99
    SAVE_INTERVAL = 50
    SAVE_DIRECTORY = "../models"
    LOAD_MOST_RECENT_MODEL = False
    LOAD_MODEL_EPISODE = 550
    KILL_REWARD = 100
    ALIVE_REWARD = 0.5
    DIE_REWARD = -500

    # Player Attributes
    PLAYER_SIZE = 6
    PLAYER_MOVEMENT_SPEED = 5
    PLAYER_TURN_SPEED = 15
    PLAYER_HEALTH = 200
    PLAYER_DAMAGE = 30
    PLAYER_SHOOT_RANGE = 300
    KILL_SCORE = 1

    # Enemy Attributes
    ENEMY_SIZE = 8
    ENEMY_MOVEMENT_SPEED = 2
    ENEMY_HEALTH = 50
    ENEMY_DAMAGE = 5
    ENEMY_MIN_DISTANCE = 20

    # Spawner Attributes
    SPAWN_INTERVAL = 200
    GROWTH_INTERVAL = 800
    GROWTH_FACTOR = 1.4
    SPAWN_BOUND_START = 4
    SPAWN_UPPER_BOUND = 10

    # Misc
    AGENT_DEBUG = 0
    AGENT_PLAYER = True
    DEBUG = 0
