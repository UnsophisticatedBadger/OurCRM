"""Unit tests for LeadValidator (US-070)."""

from ourcrm.crm.leads.models import Lead
from ourcrm.crm.leads.validator import LeadValidator


def test_valid_lead_has_no_errors() -> None:
    result = LeadValidator().validate(Lead(name="Sara Lee", status="Hot"))
    assert result.is_valid


def test_empty_name_is_rejected() -> None:
    result = LeadValidator().validate(Lead(name="", status="Hot"))
    assert result.name_error == "Name is required"
    assert not result.is_valid


def test_empty_status_is_rejected() -> None:
    result = LeadValidator().validate(Lead(name="Sara Lee", status=""))
    assert result.status_error == "Status is required"
    assert not result.is_valid


def test_min_budget_greater_than_max_is_rejected() -> None:
    result = LeadValidator().validate(
        Lead(name="Sara Lee", status="Hot", budget_min=500000, budget_max=300000)
    )
    assert result.budget_error == "Minimum budget cannot be greater than maximum budget"
    assert not result.is_valid


def test_min_budget_equal_to_max_is_accepted() -> None:
    result = LeadValidator().validate(
        Lead(name="Sara Lee", status="Hot", budget_min=300000, budget_max=300000)
    )
    assert result.budget_error is None
    assert result.is_valid


def test_only_min_budget_set_is_accepted() -> None:
    result = LeadValidator().validate(Lead(name="Sara Lee", status="Hot", budget_min=300000))
    assert result.budget_error is None
    assert result.is_valid
