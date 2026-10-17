"""Нормалізація українських телефонних номерів до формату +380XXXXXXXXX."""

import re


class InvalidPhoneError(ValueError):
    """Номер не відповідає жодному з допустимих форматів."""


_SEPARATORS = re.compile(r"[ \-]")
_SUBSCRIBER_PART = re.compile(r"[0-9]{9}")

# Префікси перевіряються від довшого до коротшого,
# щоб "380..." не сприймалося як "0..." чи навпаки.
_PREFIXES = ("+380", "380", "0")


def normalize_ua_phone(raw):
    """Повертає номер у форматі +380XXXXXXXXX або кидає InvalidPhoneError.

    Приймає номери, що починаються з 0, 380 або +380 і далі містять
    рівно 9 цифр. Пробіли та дефіси ігноруються.
    """
    if not isinstance(raw, str):
        raise InvalidPhoneError("номер має бути рядком")

    cleaned = _SEPARATORS.sub("", raw)

    for prefix in _PREFIXES:
        if cleaned.startswith(prefix):
            subscriber = cleaned[len(prefix):]
            break
    else:
        raise InvalidPhoneError("невідомий префікс номера")

    if not _SUBSCRIBER_PART.fullmatch(subscriber):
        raise InvalidPhoneError("після префікса має бути рівно 9 цифр")

    return "+380" + subscriber
