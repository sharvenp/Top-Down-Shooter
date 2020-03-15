
class Settings:

    # Screen
    WIDTH = 500
    HEIGHT = 500
    FRAME_RATE = 30
    DELTA_TIME = 1/FRAME_RATE


    # Colors
    BACKGROUND_COLOR = (30, 0, 0)
    BULLET_COLOR_PLAYER = (255, 255, 80)
    PLAYER_COLOR = (80, 255, 80)
    ENEMY_COLOR = (255, 80, 80)

    # Fonts

    # Bullet Attributes
    BULLET_SIZE = 3
    BULLET_SPEED = 200
    SHOOT_START_DIST = 15

    # Player Attributes
    PLAYER_SIZE = 6
    PLAYER_MOVEMENT_SPEED = 100
    PLAYER_TURN_SPEED = 300

    # Enemy Attributes
    ENEMY_SIZE = 8
    ENEMY_MOVEMENT_SPEED = 30

    # Spawner Attributes
    SPAWN_INTERVAL = 300
    GROWTH_INTERVAL = 600
    GROWTH_FACTOR = 1.4
    SPAWN_BOUND_START = 4


    # Misc
    DEBUG = 0