from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.unit_of_work.unit_of_work import UnitOfWork


def get_unit_of_work(
    db: Session = Depends(get_db),
) -> UnitOfWork:
    return UnitOfWork(db)