class HashTable:
    def __init__(self, size):
        self.size = size
        self.buckets = []
        for i in range(size):
            self.buckets.append([])

    def hash(self, value):
        return value % self.size

    def insert(self, package):
        bucket = self.hash(package.addressID)

        bucket_list = self.buckets[bucket]

        bucket_list.append(package)

    def delete(self, package):
        bucket = self.hash(package.addressID)
        bucket_list = self.buckets[bucket]

        if package in bucket_list:
            bucket_list.remove(package)

    