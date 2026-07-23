from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db


router = APIRouter()


@router.get("/db")
def database_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        "status": "healthy",
        "database": "connected",
    }


@router.get("/tables")
def check_enterprise_tables(db: Session = Depends(get_db)):
    tables = {}

    for table_name in [
        "organizations",
        "api_keys",
        "usage_records",
    ]:
        result = db.execute(
            text(
                """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = :table_name
                )
                """
            ),
            {"table_name": table_name},
        )

        tables[table_name] = result.scalar()

    return {
        "status": "healthy",
        "tables": tables,
    }