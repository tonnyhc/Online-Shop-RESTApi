from enum import Enum


class ChoicesEnumMixin:
    @classmethod
    def choices(cls):
        return [(x.name, x.value) for x in cls]

    @classmethod
    def max_len(cls):
        return max(len(name) for name, _ in cls.choices())


class CategoryEnumMixin(ChoicesEnumMixin, Enum):
    Sunglasses = "Sunglasses"
    Prism = "Prism"
    Lens = "Lens"
    Cases = "Cases"
