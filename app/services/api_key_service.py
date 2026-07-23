import secrets

from sqlalchemy.orm import Session

from app.core.security import generate_api_key, get_key_prefix, hash_api_key
from app.db.models.api_key import ApiKey
from app.db.models.organization import Organization


def create_organization_with_api_key(
    db: Session,
    organization_name: str,
    organization_slug: str,
    key_name: str = "Default API Key",
) -> tuple[Organization, str]:

    organization = Organization(
        name=organization_name,
        slug=organization_slug,
    )

    db.add(organization)
    db.flush()

    raw_api_key = generate_api_key()

    api_key = ApiKey(
        organization_id=organization.id,
        name=key_name,
        key_hash=hash_api_key(raw_api_key),
        key_prefix=get_key_prefix(raw_api_key),
    )

    db.add(api_key)
    db.commit()
    db.refresh(organization)

    return organization, raw_api_key