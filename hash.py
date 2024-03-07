class Node:
    def __init__(self, key, value):
        self.key = key          # addressID
        self.value = value      # Package()
        self.next = None

class HashTable:
    def __init__(self, size):
        self.size = size
        self.buckets = [None] * self.size

    def hash(self, key):
        bucket = (key % self.size)
        return bucket
    
    def insert(self, package):
        key = package.addressID

        # hash the key to find it's spot
        bucket = self.hash(key)

        # pointer node to point at the desired bucket position
        node = self.buckets[bucket]

        # if bucket is empty, place here
        if node is None:
            self.buckets[bucket] = Node(key, package)
            return
        
        # handle collisions

        # initialize pointer to current node
        prev = node

        while node is not None:
            # set the prev pointer
            prev = node
            # move our current node to the next one
            node = node.next
        # prev.next should be None, insert here
        prev.next = Node(key, package)
        
    def find(self, package):
        key = package.addressID
        # hash our package to figure out where to start looking
        bucket = self.hash(key)
        # set our node pointer there
        node = self.buckets[bucket]

        # find the package, or end of chain
        while node is not None and node.value.id != package.id:
            node = node.next

        if node is None:
            return None         # package is not in table
        else:
            return node.value   # return the found package
        
    def delete(self, package):
        key = package.addressID
        bucket = self.hash(key)
        node = self.buckets[bucket]
        prev = None

        # find the package we want to delete, or end of chain
        while node is not None and node.value.id != package.id:
            prev = node
            node = node.next

        if node is None:
            return None         # package not in table
        else:
            result = node.value # found the package to delete
            if prev is None:    # its the first item 
                node = None
            else:
                prev.next = prev.next.next  # bring chain together after delete
            
            return result   # returns the deleted package for confirmation
