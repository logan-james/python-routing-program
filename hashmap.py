class HashTable:
    def __init__(self, capacity=20):
        # Initializing a list of lists for the hash table (with a default capacity)
        self.table = [[] for _ in range(capacity)]

    def _hash_key(self, key):
        # Using a simple modulo hashing function
        return hash(key) % len(self.table)

    def insert(self, key, value):
        # Hash the key to find the appropriate bucket
        bucket_index = self._hash_key(key)
        bucket = self.table[bucket_index]

        # Check if the key already exists in the bucket, and update if it does
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # Otherwise, add the new key-value pair
        bucket.append((key, value))

    def lookup(self, key):
        # Hash the key to find the corresponding bucket
        bucket_index = self._hash_key(key)
        bucket = self.table[bucket_index]

        # Iterate through the bucket to find the key-value pair
        for k, v in bucket:
            if k == key:
                return v

        # If key not found, return None
        return None

    def remove(self, key):
        # Hash the key to find the corresponding bucket
        bucket_index = self._hash_key(key)
        bucket = self.table[bucket_index]

        # Iterate through the bucket to remove the key-value pair
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True

        # If key not found, return False
        return False
