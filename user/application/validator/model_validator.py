from common.exception.exception import InformationValidationError


class UserModelValidator:
    def validate_password_strength(self, password: str) -> str:
        if len(password) < 8:
            raise InformationValidationError("Password must be at least 8 characters.")

        if not any(c.isupper() for c in password):
            raise InformationValidationError(
                "Password must contain an uppercase letter."
            )

        if not any(c.islower() for c in password):
            raise InformationValidationError(
                "Password must contain a lowercase letter."
            )

        if not any(c.isdigit() for c in password):
            raise InformationValidationError("Password must contain a digit.")

        return password
