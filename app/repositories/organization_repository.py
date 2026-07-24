from sqlalchemy.orm import Session

from app.db.models.organization import Organization


class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    # ============================================================
    # CREATE
    # ============================================================

    def create(self, organization: Organization):
        self.db.add(organization)
        return organization

    # ============================================================
    # READ
    # ============================================================

    def get_by_id(self, organization_id: int):
        return (
            self.db.query(Organization)
            .filter(Organization.id == organization_id)
            .first()
        )

    def get_by_slug(self, slug: str):
        return (
            self.db.query(Organization)
            .filter(Organization.slug == slug)
            .first()
        )