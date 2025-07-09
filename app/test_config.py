import os

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://mock_user:mock_pass@db:5432/mock_db_test")

class TestConfig:
    SQLALCHEMY_DATABASE_URI = TEST_DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
