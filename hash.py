class HashTable:
    def __init__(self, size):
        self.size = size
        self.buckets = []
        self.contents = 0
        for i in range(size):
            self.buckets.append([])

    def hash(self, value):
        return value % self.size

    def insert(self, package):
        bucket = self.hash(package.addressID)

        bucket_list = self.buckets[bucket]

        bucket_list.append(package)
        self.contents+=1

    def search(self, package):
        bucket = self.hash(package.addressID)
        bucket_list = self.buckets[bucket]

        if package in bucket_list:
            index = bucket_list.index(package)
            return bucket_list[index]
        else:
            return None

    def delete(self, package):
        if package is not None:
            bucket = self.hash(package.addressID)
            bucket_list = self.buckets[bucket]

            if package in bucket_list:
                bucket_list.remove(package)
                self.contents-=1
            
            
    