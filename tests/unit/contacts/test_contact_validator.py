"""Unit tests for ContactValidator (US-056)."""

from ourcrm.crm.contacts.models import Contact
from ourcrm.crm.contacts.validator import ContactValidator


def test_contact_with_first_name_only_passes_name_validation() -> None:
    result = ContactValidator().validate(Contact(first_name="Jane"))
    assert result.name_error is None


def test_contact_with_last_name_only_passes_name_validation() -> None:
    result = ContactValidator().validate(Contact(last_name="Smith"))
    assert result.name_error is None


def test_contact_with_no_name_fails_with_name_required_error() -> None:
    result = ContactValidator().validate(Contact())
    assert result.name_error == "Name is required"


def test_contact_with_whitespace_only_name_fails_with_name_required_error() -> None:
    result = ContactValidator().validate(Contact(first_name="   ", last_name="  "))
    assert result.name_error == "Name is required"


def test_contact_with_no_email_passes_email_validation() -> None:
    result = ContactValidator().validate(Contact(first_name="Jane", email=""))
    assert result.email_error is None


def test_contact_with_valid_email_passes_email_validation() -> None:
    result = ContactValidator().validate(Contact(first_name="Jane", email="jane@example.com"))
    assert result.email_error is None


def test_contact_with_invalid_email_fails_email_validation() -> None:
    result = ContactValidator().validate(Contact(first_name="Jane", email="notanemail"))
    assert result.email_error is not None


def test_contact_with_no_phone_passes_phone_validation() -> None:
    result = ContactValidator().validate(Contact(first_name="Jane", phone=""))
    assert result.phone_error is None


def test_contact_with_valid_phone_passes_phone_validation() -> None:
    result = ContactValidator().validate(Contact(first_name="Jane", phone="555-0100"))
    assert result.phone_error is None


def test_contact_with_invalid_phone_fails_phone_validation() -> None:
    result = ContactValidator().validate(Contact(first_name="Jane", phone="abc"))
    assert result.phone_error is not None


def test_fully_valid_contact_is_valid() -> None:
    result = ContactValidator().validate(
        Contact(first_name="Jane", last_name="Smith", email="jane@example.com", phone="555-0100")
    )
    assert result.is_valid


def test_contact_with_only_name_error_is_not_valid() -> None:
    result = ContactValidator().validate(Contact())
    assert not result.is_valid
