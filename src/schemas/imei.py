from pydantic import BaseModel, field_validator


class IMEIRequest(BaseModel):
    imei: str
    token: str

    @field_validator("imei")
    def validate_imei(cls, v: str):
        if not (8 <= len(v) <= 15):
            raise ValueError("IMEI or S/N must be between 8 and 15 characters long")
        if not v.isalnum():
            raise ValueError("IMEI or S/N must contain only alphanumeric characters")

        # https://en.wikipedia.org/wiki/International_Mobile_Equipment_Identity#:~:text=sizes%20and%20usage.-,Check%20digit%20computation,-%5Bedit%5D
        # If IMEI is exactly 15 digits, validate Luhn checksum
        if len(v) == 15 and v.isdigit():

            def luhn_checksum(imei):
                def digits_of(n):
                    return [int(d) for d in str(n)]

                digits = digits_of(imei)
                odd_digits = digits[-1::-2]
                even_digits = digits[-2::-2]
                checksum = sum(odd_digits)
                for d in even_digits:
                    checksum += sum(digits_of(d * 2))
                return checksum % 10

            if luhn_checksum(v) != 0:
                raise ValueError("IMEI failed Luhn checksum validation")

        return v
