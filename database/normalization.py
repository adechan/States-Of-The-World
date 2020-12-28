import unicodedata


def normalize_numbers(number):
    """
    Removing "," from numbers.
    """
    normalized_number = number.replace(",", "")
    return normalized_number


def normalize_text(text):
    """
    Removing accents.
    """
    normalized_text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("utf-8")
    return normalized_text


def normalize_timezone(timezone):
    if "−" in timezone:
        return timezone.replace("−", "-")
    elif "±" in timezone:
        timezones = [timezone.replace("±", "+"), timezone.replace("±", "-")]
        return timezones
    elif "+" in timezone:
        return timezone
