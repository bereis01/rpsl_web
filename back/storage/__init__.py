import pickle
import itertools


class ObjStr:
    def __init__(self, path: str = "./"):
        self.path = path if path[-1] == "/" else path + "/"
        self.cache = {}

    def get(self, bucket: str, key: str = None):
        # Loads bucket
        if bucket not in self.cache.keys():
            file = open(self.path + bucket, "rb")
            self.cache[bucket] = pickle.load(file)
            file.close()

        return self.cache[bucket][key] if key else self.cache[bucket]

    def get_slice(self, bucket: str, skip: int, limit: int, key: str = None):
        # Loads bucket
        if bucket not in self.cache.keys():
            file = open(self.path + bucket, "rb")
            self.cache[bucket] = pickle.load(file)
            file.close()

        if key:
            return self.cache[bucket][key][skip : skip + limit]
        else:
            return dict(
                itertools.islice(self.cache[bucket].items(), skip, skip + limit)
            )

    def set(self, bucket: str, obj):
        file = open(self.path + bucket, "wb")
        self.cache[bucket] = pickle.dump(obj, file)
        file.close()
