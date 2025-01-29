import enum


class LanguageEnum(enum.Enum):
    EN = "en"
    RU = "ru"


LanguageEmoji = {
    LanguageEnum.EN: "English 🇬🇧",
    LanguageEnum.RU: "Русский 🇷🇺",
}
