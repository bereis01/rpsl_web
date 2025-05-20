import pickle
import itertools


class ObjStr:
    def __init__(self, path: str = "./"):
        self.path = path if path[-1] == "/" else path + "/"
        self.cache = {}

    def get(self, bucket: str, key: str = None):
        # Checks if bucket is in cache
        if bucket in self.cache.keys():
            return self.cache[bucket][key] if key else self.cache[bucket]

        # If it is not, reads from disk
        file = open(self.path + bucket, "rb")
        self.cache[bucket] = pickle.load(file)
        file.close()

        return self.cache[bucket][key] if key else self.cache[bucket]

    def get_slice(self, bucket: str, skip: int, limit: int):
        # Checks if bucket is in cache
        if bucket in self.cache.keys():
            return dict(
                itertools.islice(self.cache[bucket].items(), skip, skip + limit)
            )

        # If it is not, reads from disk
        file = open(self.path + bucket, "rb")
        self.cache[bucket] = pickle.load(file)
        file.close()

        return dict(itertools.islice(self.cache[bucket].items(), skip, skip + limit))
