from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.auth.result import AuthResult
from ourcrm.database.encrypted_database import EncryptedDatabase


def change_master_password_and_reencrypt(
    auth_service: AuthService,
    encrypted_db: EncryptedDatabase,
    current: str,
    new_password: str,
    confirmation: str,
) -> AuthResult:
    if not auth_service.verify_password(current):
        return AuthResult(success=False, error="Incorrect current password")

    validation = auth_service.validator.validate_with_confirmation(new_password, confirmation)
    if not validation.is_valid:
        return AuthResult(success=False, error=validation.errors[0])

    try:
        encrypted_db.rekey(new_password)
    except OSError as exc:
        return AuthResult(success=False, error=f"Could not re-encrypt the database: {exc}")

    result = auth_service.change_password(current, new_password, confirmation)
    auth_service.logout()
    return result
