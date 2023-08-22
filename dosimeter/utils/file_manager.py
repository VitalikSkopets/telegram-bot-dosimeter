import json
from pathlib import Path
from typing import Any

from dosimeter.config.logging import get_logger

logger = get_logger(__name__)


class ValidationError(ValueError):
    pass


class JSONFileManager(object):
    READ_ONLY = "r"
    WRITE_ONLY = "w"

    def __init__(self, path_to_file: Path = Path("data.json")) -> None:
        self.file = path_to_file

        if Path(self.file).exists():
            return

        self.file.touch()
        self.write(data={})
        logger.debug("Init new JSON file object.")

    def read(self) -> Any:
        if self.file.exists() and self._is_valid():
            logger.debug("Process reading file...")
            try:
                with open(self.file, self.READ_ONLY) as file:
                    data = json.load(file)
            except json.JSONDecodeError as exc:
                logger.exception(
                    "Deserializable data won't be a valid JSON "
                    "document. Raised exception: %s" % exc
                )
                exit(1)

            return data

    def write(self, data: Any) -> None:
        if self.file.exists() and self._is_valid() or not self.file.exists():
            logger.debug("Process writing file...")
            try:
                with open(self.file, self.WRITE_ONLY) as file:
                    json.dump(data, file, indent=2)
            except json.JSONDecodeError as exc:
                logger.exception(
                    "Objects cannot be serialized. Raised exception: %s" % exc
                )
                exit(1)

            logger.debug("The data has been successfully written to the file.")

    def delete(self) -> None:
        if self.file.exists() and self._is_valid():
            self.file.unlink()
            logger.debug("File was successfully deleted.")

    def _is_valid(self) -> bool:
        logger.debug("Process validating file...")
        if self.file.is_file() and self.file.suffix in (".json", ".JSON"):
            logger.debug("Validation was successful.")
            return True

        raise ValidationError(
            "File must have '.json' extension or is it not a file object."
        )
