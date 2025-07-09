import subprocess

def upgrade_db(url):
    subprocess.run(["alembic", "-x", f"db_url={url}", "upgrade", "head"])

if __name__ == "__main__":
    print("⏫ Migrando mock_db...")
    upgrade_db("postgresql://mock_user:mock_pass@db:5432/mock_db")

    print("⏫ Migrando mock_db_test...")
    upgrade_db("postgresql://mock_user:mock_pass@db:5432/mock_db_test")
