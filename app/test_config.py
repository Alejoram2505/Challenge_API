class TestConfig:
    SQLALCHEMY_DATABASE_URI = "postgresql://mock_user:mock_pass@db:5432/mock_db_test"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
