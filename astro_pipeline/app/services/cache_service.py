# In a real app, import redis here
class CacheService:
    def __init__(self):
        # Simulating Redis with a simple in-memory dict
        self._store = {}

    async def get(self, key: str):
        print(f"[Cache] Checking key: {key}")
        return self._store.get(key)

    async def set(self, key: str, value: str):
        print(f"[Cache] Setting key: {key}")
        self._store[key] = value

# Singleton instance
redis_cache = CacheService()
