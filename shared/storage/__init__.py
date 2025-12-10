import os
import sys
import shutil
import pickle
import random
import itertools


class ObjStr:
    def __init__(self, path: str = "./"):
        self.path = path if path[-1] == "/" else path + "/"
        self.object_cache = {}
        self.directory_cache = {}

    def _clean_cache(self):
        # Cleans the cache if its size exceeds 1GB
        if sys.getsizeof(self.object_cache) > 1000000000:
            # Removes 25% of the keys stored in self.object_cache
            num_removed = int(0.25 * len(self.object_cache))

            # Chooses the keys to be remove randomly
            keys_to_remove = random.sample(self.object_cache.keys(), num_removed)

            # Cleans keys
            for key in keys_to_remove:
                self.object_cache.pop(key)

        # Does the same for the other cache
        if sys.getsizeof(self.directory_cache) > 1000000000:
            num_removed = int(0.25 * len(self.directory_cache))
            keys_to_remove = random.sample(self.directory_cache.keys(), num_removed)
            for key in keys_to_remove:
                self.directory_cache.pop(key)

    def get(self, bucket: str, key: str = None, skip: int = None, limit: int = None):
        # Cleans cache
        self._clean_cache()

        # If whole bucket is requested, reads it directly from disk (no caching in this case)
        if not key:
            file = open(self.path + bucket, "rb")
            result = pickle.load(file)
            file.close()

            # Paging
            if not skip:
                skip = 0
            if not limit:
                limit = len(result)

            if isinstance(result, dict):
                return dict(itertools.islice(result.items(), skip, skip + limit))
            else:
                return result[skip : skip + limit]

        # Creates bucket entry in cache if it is not there
        if bucket not in self.object_cache.keys():
            # Checks if bucket exists
            if not os.path.isfile(self.path + bucket):
                return None

            self.object_cache[bucket] = {}

        # Checks if key is in cached bucket
        if key in self.object_cache[bucket].keys():
            return self.object_cache[bucket][key]

        # If not, loads the key to the cache before returning it
        file = open(self.path + bucket, "rb")
        temp_bucket = pickle.load(file)
        file.close()

        if key not in temp_bucket.keys():
            return None

        self.object_cache[bucket][key] = temp_bucket[key]
        return self.object_cache[bucket][key]

    def set(self, bucket: str, obj):
        # Cleans cache
        self._clean_cache()

        # Writes the bucket as a standalone object
        file = open(self.path + bucket, "wb")
        pickle.dump(obj, file)
        file.close()

    def get_key(self, bucket: str, key: str):
        # Cleans cache
        self._clean_cache()

        # Creates bucket in cache if its not there
        if bucket not in self.directory_cache.keys():
            # Checks if bucket exists
            if not os.path.isdir(self.path + bucket):
                return None

            self.directory_cache[bucket] = {}

        # Loads key to cache if its not there
        if key not in self.directory_cache[bucket].keys():
            # Checks if key exists in bucket
            if not os.path.isfile(self.path + bucket + "/" + key):
                return None

            # Opens the file and puts it in the cache
            file = open(self.path + bucket + "/" + key, "rb")
            self.directory_cache[bucket][key] = pickle.load(file)
            file.close()

        return self.directory_cache[bucket][key]

    def get_bucket(self, bucket: str, skip: int = None, limit: int = None):
        # Cleans cache
        self._clean_cache()

        # Creates bucket in cache if its not there
        if bucket not in self.directory_cache.keys():
            # Checks if bucket exists
            if not os.path.isdir(self.path + bucket):
                return None

            self.directory_cache[bucket] = {}

        # Keys in the bucket
        # Applies paging if passed
        keys = os.listdir(self.path + bucket)
        keys.sort()
        if skip:
            keys = keys[skip:]
        if limit:
            keys = keys[:limit]

        # Gets the results
        result = {}
        for key in keys:
            # Loads key to cache if its not there
            if key not in self.directory_cache[bucket].keys():
                # Opens the file and puts it in the cache
                file = open(self.path + bucket + "/" + key, "rb")
                self.directory_cache[bucket][key] = pickle.load(file)
                file.close()

            result[key] = self.directory_cache[bucket][key]

        return result

    def set_key(self, bucket: str, key: str, obj):
        # Cleans cache
        self._clean_cache()

        # Creates the bucket if it does not exist
        if not os.path.isdir(self.path + bucket):
            os.mkdir(self.path + bucket)

        # Inserts the key object in the bucket
        # Overwrites if it already exists
        file = open(self.path + bucket + "/" + key, "wb")
        pickle.dump(obj, file)
        file.close()

    def set_bucket(self, bucket: str, obj):
        # Cleans cache
        self._clean_cache()

        # Raises error if object is not dict
        if not isinstance(obj, dict):
            raise Exception("Bucket as object must be a dict.")

        # Creates the bucket
        # Deletes it and creates an empty one if it already exists
        if os.path.isdir(self.path + bucket):
            shutil.rmtree(self.path + bucket)
        os.mkdir(self.path + bucket)

        # Inserts the key objects in the bucket
        # Overwrites if it already exists
        for key in obj.keys():
            file = open(self.path + bucket + "/" + key, "wb")
            pickle.dump(obj[key], file)
            file.close()
