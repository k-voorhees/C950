from package import Package, Status
from hash import HashTable
import data


def nearestNeighbor(rowNum, table):
    # pointer to the row we are working with
    row = table[rowNum]
    # get the distance of closest neighbor
    nearest = min(i for i in row if i > 0)
    # get the index of closest neighbor
    address = row.index(nearest)
    
    # returns a tuple -> address, and the distance to it.
    return (address, nearest)

def main():
    # import data from files
    packages = data.loadPackageData()
    addresses = data.loadAddressData()
    distanceTable = data.loadDistanceData()
    
    # set the addressID for each package
    for package in packages:
        for address in addresses:
            if package.address == address:
                package.addressID = addresses.index(address)
                break

    # create hash table

    # create Trucks

    # load truck

    # deliver packages
    pass

if __name__ == "__main__":
    main()