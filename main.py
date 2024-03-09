from package import Package, Status, Priority
from hash import HashTable
from truck import Truck
import data
import datetime


def nearestNeighbor(rowNum, table):
    # pointer to the row we are working with
    row = table[rowNum]
    # get of closest neighbor
    nearest = row.index(min(i for i in row if i > 0))

    return nearest

def setAddressID(packages, addresses):
# set the addressID for each package
    for package in packages:
        for address in addresses:
            if package.address == address:
                package.addressID = addresses.index(address)
                break

def distanceBetween(address1, address2, table):
    return table[address1][address2]

def setStatus(packages):
    for package in packages:
        if "Delayed" in package.note:
            package.status = Status.DELAYED

def setPriority(packages):
    for package in packages:
        if package.deadline == datetime.datetime(1900, 1, 3, 9, 0):
            package.Priority = Priority.FIRST
        elif package.deadline == datetime.datetime(1900, 1, 3, 10, 30):
            package.Priority = Priority.SECOND

def load(truck, table):
    i = 1
    while truck.hasRoom():
        bucket = table.buckets[i]
        node = bucket
        while node is not None:
            currentPackage = node.value
            if currentPackage.status is Status.AT_HUB:
                truck.load(currentPackage)
            
            node = node.next
        i += 1


def main():
    # import data from files
    packages = data.loadPackageData()
    addresses = data.loadAddressData()
    distanceTable = data.loadDistanceData()
    setAddressID(packages, addresses)
    setStatus(packages)
    setPriority(packages)

    # create and load hash table
    hashTable = HashTable(len(addresses))
    for package in packages:
        hashTable.insert(package)
    # create Trucks
    Truck1 = Truck(1)

    # load truck
    load(Truck1, hashTable)
    for package in Truck1.cargo:
        hashTable.delete(package)
    # deliver packages
    pass

if __name__ == "__main__":
    main()