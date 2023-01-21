from dosimeter import config

__all__ = ("get_id_from_text", "greeting")

logger = config.get_logger(__name__)

greeting: tuple[str, ...] = (
    "hello",
    "hi",
    "hey",
    "привет",
    "салют",
    "здарова",
    "здравствуй",
    "здравствуйте",
    "добрый день",
    "добрый вечер",
    "доброе утро",
    "доброго дня",
    "хелоу",
    "бонжур",
    "привестствую",
    "здрасте",
    "какая встреча",
    "рад встрече",
    "хай",
    "здравия желаю",
    "приветик",
    "доброго времени суток",
    "здорова",
    "здорово",
    "мое почтение",
    "приветствую тебя",
    "сердечно приветствую",
    "how are you",
    "what’s up",
    "whats up",
    "hello there",
    "howdy",
    "hiya",
    "yo",
    "how do you do",
    "good morning",
    "good afternoon",
    "good evening",
    "peek-a-boo",
    "peek a boo",
    "hi mister",
    "ahoy",
)


def get_id_from_text(text: str) -> int | str:  # type: ignore[return]
    match text.split(" ").pop().strip():
        case str() as uid if uid.isdigit():
            return int(uid)
        case _:
            return "The user ID is incorrect. The ID value must contain only numbers."
