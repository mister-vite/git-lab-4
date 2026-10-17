import pytest

from phone_normalizer import InvalidPhoneError, normalize_ua_phone

EXPECTED = "+380671234567"


# --- Щасливий шлях: три допустимі формати ---------------------------------

@pytest.mark.parametrize(
    "raw",
    ["0671234567", "380671234567", "+380671234567"],
    ids=["with_zero", "with_380", "with_plus_380"],
)
def test_valid_formats_are_converted_to_plus_380(raw):
    # Arrange: raw задано параметром
    # Act
    result = normalize_ua_phone(raw)
    # Assert
    assert result == EXPECTED


def test_spaces_inside_number_are_removed():
    result = normalize_ua_phone("0 67 123 45 67")

    assert result == EXPECTED


def test_dashes_inside_number_are_removed():
    result = normalize_ua_phone("+380-67-123-45-67")

    assert result == EXPECTED


# --- Відмова: неприпустимий вхід реально відхиляється ---------------------

def test_short_number_is_rejected():
    with pytest.raises(InvalidPhoneError):
        normalize_ua_phone("067123")


def test_letter_inside_number_is_rejected():
    with pytest.raises(InvalidPhoneError):
        normalize_ua_phone("06712A4567")


def test_unknown_prefix_is_rejected():
    with pytest.raises(InvalidPhoneError):
        normalize_ua_phone("+48671234567")


def test_non_string_input_is_rejected():
    with pytest.raises(InvalidPhoneError):
        normalize_ua_phone(671234567)


def test_plus_in_the_middle_is_rejected():
    with pytest.raises(InvalidPhoneError):
        normalize_ua_phone("067+1234567")


# --- Межа: рівно 9 цифр абонентської частини ------------------------------

def test_nine_digits_after_prefix_is_accepted():
    result = normalize_ua_phone("0671234567")

    assert result == "+380671234567"


def test_eight_digits_after_prefix_is_rejected():
    with pytest.raises(InvalidPhoneError):
        normalize_ua_phone("067123456")


def test_ten_digits_after_prefix_is_rejected():
    with pytest.raises(InvalidPhoneError):
        normalize_ua_phone("06712345678")


# --- Ще випадки: порожній вхід і повідомлення про помилку -----------------

def test_empty_string_is_rejected():
    with pytest.raises(InvalidPhoneError):
        normalize_ua_phone("")


def test_only_separators_is_rejected():
    with pytest.raises(InvalidPhoneError):
        normalize_ua_phone(" - - ")


def test_rejection_reason_mentions_digit_count():
    with pytest.raises(InvalidPhoneError, match="9 цифр"):
        normalize_ua_phone("067123")
