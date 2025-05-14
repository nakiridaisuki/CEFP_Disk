from .jsonDB import JSONDatabase

_db_instance = None

def get_db(file_path: str = None) -> JSONDatabase:
    global _db_instance
    if not _db_instance and file_path:
        _db_instance = JSONDatabase(file_path)
    elif not _db_instance:
        raise RuntimeError("Need to initilize database first.")
    return _db_instance