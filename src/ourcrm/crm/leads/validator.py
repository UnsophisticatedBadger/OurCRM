"""Lead validation — US-070."""

from __future__ import annotations

from dataclasses import dataclass

from ourcrm.crm.leads.models import Lead


@dataclass
class LeadValidationResult:
    name_error: str | None = None
    status_error: str | None = None
    budget_error: str | None = None

    @property
    def is_valid(self) -> bool:
        return self.name_error is None and self.status_error is None and self.budget_error is None


class LeadValidator:
    def validate(self, lead: Lead) -> LeadValidationResult:
        name_error = None
        if not lead.name.strip():
            name_error = "Name is required"

        status_error = None
        if not lead.status.strip():
            status_error = "Status is required"

        budget_error = None
        if (
            lead.budget_min is not None
            and lead.budget_max is not None
            and lead.budget_min > lead.budget_max
        ):
            budget_error = "Minimum budget cannot be greater than maximum budget"

        return LeadValidationResult(
            name_error=name_error, status_error=status_error, budget_error=budget_error
        )
