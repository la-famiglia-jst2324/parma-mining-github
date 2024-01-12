"""Helper functions."""

from parma_mining.github.model import ErrorInfoModel
from parma_mining.mining_common.exceptions import BaseError


def collect_errors(company_id: str, errors: dict, e: BaseError):
    """Collect errors in required dict format."""
    errors[company_id] = ErrorInfoModel(
        error_type=e.__class__.__name__, error_description=e.message
    )
