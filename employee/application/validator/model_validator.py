from datetime import date, datetime

from common.exception.exception import InformationValidationError


class EmployeeModelValidator:
    def validate_date(self, value):
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, str):
            value = value.strip()
            try:
                return date.fromisoformat(value)
            except ValueError:
                # logger.warning("Date in the wrong format")
                raise InformationValidationError(
                    "Date should be in YYYY-MM-DD format only"
                )
        if value > date.today():  # noqa: DTZ011
            raise InformationValidationError("Date cannot be in the future")
        return value

    def validate_dob(self, value):
        if isinstance(value, datetime):
            return value.date()

        if isinstance(value, str):
            value = value.strip()
            try:
                return date.fromisoformat(value)
            except ValueError:
                # logger.warning("Date in wrong format")
                raise InformationValidationError(
                    "Date should be in YYYY-MM-DD format only"
                )
        if value > date(2009, 1, 1):
            raise InformationValidationError("Employees should be at least 16 years")
        return value

    def validate_pan_number(self, pan_number: str):
        if len(pan_number) != 10:
            raise InformationValidationError(
                "PAN card number should only be 10 characters long"
            )
        if not pan_number[:5].isalpha() or not pan_number[:5].isupper():
            raise InformationValidationError(
                "PAN card number must contain 5 upper case characters in the beginning"
            )
        if not pan_number[5:9].isnumeric():
            raise InformationValidationError(
                "After the 5 alphabets 4 digits should be there"
            )
        if not pan_number[-1].isalpha() or not pan_number[-1].isupper():
            raise InformationValidationError(
                "The last character of PAN card number should be an upper case alphabet"
            )
        return pan_number

    def validate_address(self, address: str) -> str:

        if not isinstance(address, str):
            raise InformationValidationError("Address must be text")

        normalized_address = " ".join(address.split())
        if len(normalized_address) < 5:
            raise InformationValidationError(
                "Address must be at least 5 characters long"
            )

        if not any(character.isalpha() for character in normalized_address):
            raise InformationValidationError("Address must contain at least one letter")

        return normalized_address

    def validate_phone_number(self, phone_number: str) -> str:
        if not isinstance(phone_number, str):
            raise InformationValidationError("Phone number must be text")

        normalized_phone_number = phone_number.strip()
        if not normalized_phone_number.isdigit() or len(normalized_phone_number) != 10:
            raise InformationValidationError(
                "Phone number must contain exactly 10 digits"
            )

        return normalized_phone_number
