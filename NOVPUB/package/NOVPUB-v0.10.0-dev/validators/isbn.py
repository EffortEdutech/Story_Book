def normalize_isbn13(value: str) -> str:
    return ''.join(ch for ch in str(value) if ch.isdigit())

def isbn13_check_digit(first12: str) -> int:
    if len(first12) != 12 or not first12.isdigit():
        raise ValueError('ISBN-13 prefix must contain exactly 12 digits')
    total = sum(int(ch) * (1 if i % 2 == 0 else 3) for i, ch in enumerate(first12))
    return (10 - (total % 10)) % 10

def validate_isbn13(value: str) -> bool:
    digits = normalize_isbn13(value)
    if len(digits) != 13:
        return False
    if digits[:3] not in {'978', '979'}:
        return False
    return int(digits[-1]) == isbn13_check_digit(digits[:12])
