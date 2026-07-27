from sqlalchemy.orm import Session

from app.db.models.payment_transaction import PaymentTransaction


class PaymentTransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    # ============================================================
    # CREATE
    # ============================================================

    def create(self, transaction: PaymentTransaction):
        self.db.add(transaction)
        return transaction

    # ============================================================
    # READ
    # ============================================================

    def get_by_reference(self, reference: str):
        return (
            self.db.query(PaymentTransaction)
            .filter(PaymentTransaction.reference == reference)
            .first()
        )