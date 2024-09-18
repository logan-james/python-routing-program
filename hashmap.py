class HashTable:
    def __init__(self, capacity=20):
        # Initialize the hash table with empty buckets
        self.table = [[] for _ in range(capacity)]

    def _hash_key(self, key):
        # Generate a hash value for the given key
        return hash(key) % len(self.table)

    def insert(self, key, value):
        # Insert a key-value pair into the hash table
        # If the key exists, update its value; otherwise, add a new pair
        bucket_index = self._hash_key(key)
        bucket = self.table[bucket_index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))

    def lookup(self, key):
        # Look up a value in the hash table by its key
        bucket_index = self._hash_key(key)
        bucket = self.table[bucket_index]

        for k, v in bucket:
            if k == key:
                return v

        return None

    def remove(self, key):
        # Remove a key-value pair from the hash table
        bucket_index = self._hash_key(key)
        bucket = self.table[bucket_index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True

        return False