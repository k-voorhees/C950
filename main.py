from package import Package, Status
from hash import HashTable
import data


def main():
    # import data from files
    packages = data.loadPackageData()
    addresses = data.loadAddressData()
    distanceTable = data.loadDistanceData()
    
    # set the addressID for each package
    for package in packages:
        for idx, address in enumerate(addresses):
            if package.address.strip() == address[0].strip():
                package.addressID = idx
                break

    # create hash table

    # create Trucks

    # load truck

    # deliver packages
    pass

if __name__ == "__main__":
    main()