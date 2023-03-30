import os


class DefaultConfig:
    TARGET_DIR = os.environ.get("RACE_INFO_DIR")
    DEBUG = True
    TESTING = False


class TestConfig:
    TARGET_DIR = os.environ.get("RACE_INFO_DIR")
    DEBUG = True
    TESTING = True
