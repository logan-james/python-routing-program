class HashTable:
    def __init__(self, capacity=20):
        # Initialize the hash table with empty buckets
        self.table = [[] for _ in range(capacity)]

    # Generate a hash value for the given key
    def _hash_key(self, key):
        return hash(key) % len(self.table)

    # Insert a key-value pair into the hash table
    # If the key exists, update its value; otherwise, add a new pair
    def insert(self, key, value):
        bucket_index = self._hash_key(key)
        bucket = self.table[bucket_index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))

    # Look up a value in the hash table by its key
    def lookup(self, key):
        bucket_index = self._hash_key(key)
        bucket = self.table[bucket_index]

        for k, v in bucket:
            if k == key:
                return v

        return None

    # Remove a key-value pair from the hash table
    def remove(self, key):
        bucket_index = self._hash_key(key)
        bucket = self.table[bucket_index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True

        return False