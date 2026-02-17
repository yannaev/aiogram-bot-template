from sqids import Sqids

from app.config import settings

alphabet = settings.alphabet


class DeepLink:
    _sqids = Sqids(alphabet=alphabet, min_length=8)

    @classmethod
    def encode(cls, telegram_id: int) -> str:
        return cls._sqids.encode([telegram_id])

    @classmethod
    def decode(cls, code: str) -> int | None:
        try:
            numbers = cls._sqids.decode(code)
            return numbers[0] if numbers else None
        except Exception:
            return None