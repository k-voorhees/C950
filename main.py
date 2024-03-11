from package import Package, Status
from hash import HashTable
from truck import Truck
import data
import datetime


def nearestNeighbor(num, distanceTable):
    # pointer to the row we are working with
    row = distanceTable[num]
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

def manualLoadRestricted(trucks, packages, table):
# MANUALLY LOAD PACKAGES BASED ON RESTRICTIONS. 
# NEAREST NEIGHBOR WILL BE USED IN DELIVERY FUNCTION LATER
    requires_truck_2 = [packages[2], packages[17], packages[35], packages[37]]
    required_together = [packages[12],packages[13],packages[14],packages[15],packages[18],packages[19]]
# DELAYED PACKAGES WILL BE UPDATED VIA FUNCTION ONCE TIME HITS 9:05 LATER IN PROGRAM
# PACKAGE 9 - WRONG ADDRESS WILL BE UPDATED LIKE OTHER DELAYED PACKAGES ONCE TIME HITS 10:20
    truck1, truck2, truck3 = trucks[0], trucks[1], trucks[2]

    #   TRUCK 1
    # package 15 is first priority. is also in required_together, so load all of those first
    for package in required_together:
        # # load the required package
        if package.status is Status.AT_HUB:
            truck1.load(table.search(package))      # load the package onto the truck
            package.status = Status.EN_ROUTE        # update Status
    cleanUpHashTable(truck1, table)
    
    # load all of the packages that are also located at the same stops as in required_together[]
    for package in truck1.cargo:
        bucket = table.hash(package.addressID)
        bucket_list = table.buckets[bucket]
        for item in bucket_list:
            if item.status is Status.AT_HUB and item not in requires_truck_2:
                truck1.load(table.search(item))
                item.status = Status.EN_ROUTE
    cleanUpHashTable(truck1, table)
    #   TRUCK 2
    for package in requires_truck_2:
        if package.status is Status.AT_HUB:
            truck2.load(table.search(package))
            package.status = Status.EN_ROUTE
    cleanUpHashTable(truck1, table)

    # load all of the packages that are also located at the same stops as in required_together[]
    for package in truck2.cargo:
        bucket = table.hash(package.addressID)
        bucket_list = table.buckets[bucket]
        for item in bucket_list:
            if item.status is Status.AT_HUB:
                truck2.load(table.search(item))
                item.status = Status.EN_ROUTE
    
    cleanUpHashTable(truck2, table)

def fillTruck(truck, table):
    # fills the remaining open space in the truck
    i = 1
    while truck.hasRoom():
        bucket_list = table.buckets[i]
        for package in bucket_list:
            if truck.hasRoom() and package.status is Status.AT_HUB:
                truck.load(table.search(package))
                package.status = Status.EN_ROUTE

        i+=1
    cleanUpHashTable(truck, table)
    
def cleanUpHashTable(truck, table):
    # remove packages from hashtable that were loaded on truck
    for package in truck.cargo:
        table.delete(table.search(package))


def main():
    # import data from files
    packages = data.loadPackageData()
    addresses = data.loadAddressData()
    distanceTable = data.loadDistanceData()
    setAddressID(packages, addresses)
    setStatus(packages)

    # create and load hash table
    hashTable = HashTable(len(addresses))
    for package in packages:
        hashTable.insert(package)
    # create Trucks
    Truck1 = Truck(1)
    Truck2 = Truck(2)
    Truck3 = Truck(3)

    TruckList = [Truck1, Truck2, Truck3]

    # load truck
    manualLoadRestricted(TruckList, packages, hashTable)
# PACKAGES LEFT IN HASH TABLE AT THIS POINT DO NOT HAVE A RESTRICTION OTHER THAN BEING DELAYED
# FILL THE EMPTY SPACE ON EACH TRUCK
    fillTruck(Truck1, hashTable)
    fillTruck(Truck2, hashTable)
    
    # deliver packages
    pass

if __name__ == "__main__":
    main()