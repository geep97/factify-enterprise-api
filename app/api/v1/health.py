from fastapi import APIRouter, Depends, status,HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session


from app.db.database import get_db

router = APIRouter()

REQUIRED_TABLES = [
    "organizations",
    "api_keys",
    "usage_records",
]


def _check_database(db: Session) -> bool:
    """Check that the database is reachable."""
    db.execute(text("SELECT 1"))
    return True


def _check_required_tables(db: Session) -> dict[str, bool]:
    """Check that all required tables exist."""
    tables = {}

    for table_name in REQUIRED_TABLES:
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

    return tables


@router.get("/live")
def liveness():
    """
    Liveness probe.

    Indicates that the application process is running.
    """
    return {
        "status": "alive",
    }


@router.get("/db")
def database_health(db: Session = Depends(get_db)):
    _check_database(db)

    return {
        "status": "healthy",
        "database": "connected",
    }


@router.get("/tables")
def check_enterprise_tables(db: Session = Depends(get_db)):
    return {
        "status": "healthy",
        "tables": _check_required_tables(db),
    }


@router.get("/ready")
def readiness(db: Session = Depends(get_db)):
    """
    Readiness probe.

    Indicates whether the application is ready to serve requests.
    """
    database_ok = _check_database(db)
    tables = _check_required_tables(db)

    checks = {
        "database": database_ok,
        "tables": all(tables.values()),
    }

    if not all(checks.values()):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "not_ready",
                "checks": checks,
            },
        )

    return {
        "status": "ready",
        "checks": checks,
    }