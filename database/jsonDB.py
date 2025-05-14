import json
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

class JSONDatabase:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, file_path: str = None):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    if not file_path:
                        raise ValueError("Need file_path when first initilization.")
                    cls._instance = super().__new__(cls)
                    cls._instance.__initialized = False
        return cls._instance

    def __init__(self, file_path: str = None):
        if not self.__initialized:
            self.file_path = Path(file_path)
            self.data_lock = threading.Lock()
            self._initialize_file()
            self.__initialized = True

    def _initialize_file(self):
        if not self.file_path.exists():
            with self.data_lock:
                self.file_path.write_text(json.dumps({"users": []}))

    def _clean(self):
        self.file_path.write_text(json.dumps({"users": []}))

    def _read_data(self) -> Dict[str, Any]:
        with self._lock:
            with open(self.file_path, 'r') as f:
                return json.load(f)

    def _write_data(self, data: Dict[str, Any]) -> None:
        with self._lock:
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=4)

    def get_all_users(self) -> List[Dict]:
        data = self._read_data()
        return [u.get('name') for u in data['users']]
    
    def get_user_data(self, name: str) -> Dict:
        data = self._read_data()
        user_data = [u for u in data['users'] if u['name'] == name][0]
        return user_data

    def add_user(self, user_data: Dict) -> Dict:
        data = self._read_data()

        try:
            name = user_data.get('name')
        except (KeyError):
            raise "Need user name."
        
        users = self.get_all_users()
        if name in users:
            return user_data
        
        new_id = max([u.get('id', 0) for u in data['users']] or [0]) + 1
        user_data['id'] = new_id
        data['users'].append(user_data)
        self._write_data(data)
        return user_data

    def update_user(self, user_id: int, update_data: Dict) -> Optional[Dict]:
        data = self._read_data()
        for user in data['users']:
            if user['id'] == user_id:
                user.update(update_data)
                self._write_data(data)
                return user
        return None

    def delete_user(self, user_id: int) -> bool:
        data = self._read_data()
        initial_length = len(data['users'])
        data['users'] = [u for u in data['users'] if u['id'] != user_id]
        if len(data['users']) < initial_length:
            self._write_data(data)
            return True
        return False
    
if __name__ == '__main__':
    test = JSONDatabase('test.json')
    test.add_user({ 'name': 'test', 'password': 'pp' })
    test.add_user({ 'name': 'test2', 'password': 'pp1' })
    test.add_user({ 'name': 'test3', 'password': 'p2' })
    users = test.get_user_data('test')
    print(users)
