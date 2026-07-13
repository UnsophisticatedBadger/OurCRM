from ourcrm.core.auth.auth_service import AuthService
from ourcrm.core.auth.result import RecoveryResult
from ourcrm.core.security.recovery_generator import RecoveryPasswordGenerator
from ourcrm.database.encrypted_database import EncryptedDatabase, InvalidDatabaseKeyError


def recover_and_reencrypt(
    auth_service: AuthService,
    encrypted_db: EncryptedDatabase,
    recovery_generator: RecoveryPasswordGenerator,
    recovery_password: str,
    new_password: str,
    confirmation: str,
) -> RecoveryResult:
    if not auth_service.verify_recovery_password(recovery_password):
        return RecoveryResult(success=False, error="Incorrect recovery password")

    validation = auth_service.validator.validate_with_confirmation(new_password, confirmation)
    if not validation.is_valid:
        return RecoveryResult(success=False, error=validation.errors[0])

    new_recovery_password = recovery_generator.generate()
    try:
        encrypted_db.open_with_recovery(recovery_password)
        encrypted_db.rotate(new_password, new_recovery_password)
    except InvalidDatabaseKeyError:
        return RecoveryResult(success=False, error="Incorrect recovery password")
    except OSError as exc:
        return RecoveryResult(success=False, error=f"Could not re-encrypt the database: {exc}")

    auth_service.create_master_password(new_password)
    auth_service.store_recovery_password(new_recovery_password)
    return RecoveryResult(success=True, new_recovery_password=new_recovery_password)
