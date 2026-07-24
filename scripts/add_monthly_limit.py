from sqlalchemy import text

from app.db.database import engine


def main():
    print("Connecting to database...")

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                ALTER TABLE organizations
                ADD COLUMN IF NOT EXISTS monthly_request_limit
                INTEGER NOT NULL DEFAULT 1000
                """
            )
        )

    print("monthly_request_limit column added successfully.")


if __name__ == "__main__":
    main()