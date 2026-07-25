from sqlalchemy.orm import Session

from app.db.models.subscription import Subscription


class SubscriptionRepository:
    def __init__(self, db: Session):
        self.db = db

    # ============================================================
    # CREATE
    # ============================================================

    def create(
        self,
        subscription: Subscription,
    ) -> Subscription:

        self.db.add(subscription)

        return subscription

    # ============================================================
    # READ
    # ============================================================

    def get_by_id(
        self,
        subscription_id: int,
    ) -> Subscription | None:

        return (
            self.db.query(Subscription)
            .filter(Subscription.id == subscription_id)
            .first()
        )

    def get_by_organization_id(
        self,
        organization_id: int,
    ) -> Subscription | None:

        return (
            self.db.query(Subscription)
            .filter(
                Subscription.organization_id == organization_id
            )
            .first()
        )

    def get_by_plan(
        self,
        plan_name: str,
    ) -> list[Subscription]:

        return (
            self.db.query(Subscription)
            .filter(Subscription.plan_name == plan_name)
            .all()
        )

    def get_by_status(
        self,
        status: str,
    ) -> list[Subscription]:

        return (
            self.db.query(Subscription)
            .filter(Subscription.status == status)
            .all()
        )

    def get_all(self) -> list[Subscription]:

        return (
            self.db.query(Subscription)
            .all()
        )

    # ============================================================
    # DELETE
    # ============================================================

    def delete(
        self,
        subscription: Subscription,
    ):

        self.db.delete(subscription)