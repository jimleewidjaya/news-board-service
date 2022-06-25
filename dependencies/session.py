import pickle
import uuid
import redis
from nameko.extensions import DependencyProvider


class SessionWrapper:
    def __init__(self, connection) -> None:
        self.redis = connection
        self.default_expire = 60 * 60

    def check_session_id(self, session_id):
        return self.redis.exists(session_id)

    def generate_session_id(self):
        key = str(uuid.uuid4())
        while self.check_session_id(key):
            key = str(uuid.uuid4())
        self.redis.set(key, pickle.dumps({}))
        return key

    def get_session_data(self, session_id):
        return pickle.loads(self.redis.get(session_id))

    def set_session_data(self, username):
        user_data_pickled = pickle.dumps(username)
        session_id = self.generate_session_id()
        self.redis.set(session_id, user_data_pickled, ex=self.default_expire)

        return session_id

    def reset_session_data(self, session_id):
        self.redis.set(session_id, pickle.dumps({}))

    def delete_session(self, session_id):
        response = {}
        self.redis.delete(session_id)
        response['status'] = 'success'
        response['message'] = 'Login out successfully!'
        
        return response


class SessionProvider(DependencyProvider):
    def __init__(self):
        self.client = redis.Redis(host="127.0.0.1", port=6379, db=0)

    def get_dependency(self, worker_ctx):
        return SessionWrapper(self.client)
