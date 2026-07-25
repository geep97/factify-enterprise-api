from fastapi import Depends

from app.clients.factify_client import FactifyClient
from app.services.api_key_service import ApiKeyService
from app.services.dashboard_service import DashboardService
from app.services.subscription_service import SubscriptionService
from app.services.usage_service import UsageService
from app.services.verification_service import VerificationService
from app.unit_of_work.dependencies import get_unit_of_work
from app.unit_of_work.unit_of_work import UnitOfWork


# ============================================================
# CLIENTS
# ============================================================

def get_factify_client():
    return FactifyClient()


# ============================================================
# SERVICES
# ============================================================

def get_api_key_service(
    uow: UnitOfWork = Depends(get_unit_of_work),
):
    return ApiKeyService(uow)


def get_subscription_service(
    uow: UnitOfWork = Depends(get_unit_of_work),
):
    return SubscriptionService(uow)


def get_usage_service(
    uow: UnitOfWork = Depends(get_unit_of_work),
):
    return UsageService(uow)


def get_verification_service(
    client: FactifyClient = Depends(get_factify_client),
):
    return VerificationService(client)


def get_dashboard_service(
    uow: UnitOfWork = Depends(get_unit_of_work),
):
    return DashboardService(uow)