"""Top-level package """

__app_name__ = "kaztau"
__version__ = "0.2.0"
__website_url__ = "https://github.com/btechpt/kaztau"
__author__ = "Boer Technology"
__title__ = "Kaztau"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(7)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    DB_READ_ERROR: "database read error",
    DB_WRITE_ERROR: "database write error",
    ID_ERROR: "contact id error",
}
