class HashTable:
    def __init__(self, capacity=40):
        self.table = [None] * capacity
        self.capacity = capacity

    def _hash(self, key):
        return key % self.capacity

    def insert(self, key, package):
        hash_index = self._hash(key)
        # If there's no collision
        if self.table[hash_index] is None:
            self.table[hash_index] = [package]
        else:
            # Collision handling using chaining
            self.table[hash_index].append(package)

    def lookup(self, key):
        hash_index = self._hash(key)
        if self.table[hash_index] is not None:
            for package in self.table[hash_index]:
                if package.id == key:
                    return package
        return None

    def remove(self, key):
        hash_index = self._hash(key)
        if self.table[hash_index] is not None:
            for i, package in enumerate(self.table[hash_index]):
                if package.id == key:
                    self.table[hash_index].pop(i)
                    return True
        return False

    def get_all_packages(self):
        all_packages = []
        for bucket in self.table:
            if bucket:
                all_packages.extend(bucket)
        return all_packages
