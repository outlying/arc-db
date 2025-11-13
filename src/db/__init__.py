import os
from pathlib import Path

SQLITE_SCHEMA = Path(os.path.abspath("./db/arc.sql"))
SQLITE_DATABASE = Path(os.path.abspath("./db/arc.db"))