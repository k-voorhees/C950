from package import Package, Status
from hash import HashTable
from truck import Truck
import data
from datetime import time, datetime, timedelta

# GLOBALS FOR CALCULATIONS
SPEED_OF_TRUCK = 18
START_TIME =time(8,0,0)
PACKAGES_DELIVERED = 0
TIME_COMPLETED=time(0,0,0)

def incrementCount():
    global PACKAGES_DELIVERED
    PACKAGES_DELIVERED+=1

def distanceBetween(address1, address2, table):
    return table[address1][address2] 

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
            package.departTime = (START_TIME)
    cleanUpHashTable(truck1, table)
    
    # load all of the packages that are also located at the same stops as in required_together[]
    for package in truck1.cargo:
        bucket = table.hash(package.addressID)
        bucket_list = table.buckets[bucket]
        for item in bucket_list:
            if item.status is Status.AT_HUB and item not in requires_truck_2:
                truck1.load(table.search(item))
                item.status = Status.EN_ROUTE
                item.departTime = (START_TIME)

    cleanUpHashTable(truck1, table)

#   TRUCK 2
    for package in requires_truck_2:
        if package.status is Status.AT_HUB:
            truck2.load(table.search(package))
            package.status = Status.EN_ROUTE
            package.departTime = (START_TIME)
    cleanUpHashTable(truck1, table)

    # load all of the packages that are also located at the same stops as in required_together[]
    for package in truck2.cargo:
        bucket = table.hash(package.addressID)
        bucket_list = table.buckets[bucket]
        for item in bucket_list:
            if item.status is Status.AT_HUB:
                truck2.load(table.search(item))
                item.status = Status.EN_ROUTE
                item.departTime = START_TIME
    
    cleanUpHashTable(truck2, table)

def fillTruck(truck, table):
    # fills the remaining open space in the truck
    i = 1
    while i < table.size:
        bucket_list = table.buckets[i]
        for package in bucket_list:
            if truck.hasRoom() and package.status is Status.AT_HUB:
                truck.load(table.search(package))
                package.status = Status.EN_ROUTE
                package.departTime = truck.clock

        i+=1
    cleanUpHashTable(truck, table)
    
def cleanUpHashTable(truck, table):
    # remove packages from hashtable that were loaded on truck
    for package in truck.cargo:
        table.delete(table.search(package))

def calculateTime(distance):
    # calculate time based on distance and travel speed
    time = (float(60 * (distance / SPEED_OF_TRUCK)))
    time = str(round(time, 2))
    timeT = str(time).split(".")

    # return tuple of (minutes, seconds)
    return (int(timeT[0]), int(timeT[1])) 

def increaseTime(travelTime, currentTime):
    td = timedelta(hours=currentTime.hour, minutes=currentTime.minute, seconds=currentTime.second)
    td += timedelta(minutes=travelTime[0])  # increase minutes
    td += timedelta(seconds=travelTime[1])  # increase seconds
    return (datetime.min + td).time()

def deliverPackages(truck, dtable, time):
    startingLocation = 0    # ADDRESSID OF HUB ON DISTANCE TABLE
    currentLocation = startingLocation
    currentTime = time

    # LIST OF STOPS TRUCK HAS TO MAKE
    stops = [] 
    for package in truck.cargo:
            if package.addressID not in stops:
                stops.append(package.addressID)

    # IMPLEMENT NEAREST NEIGHBOR TO DELIVER ALL PACKAGES
    while stops:
        # NEW LIST OF DISTANCES FROM CURRENT LOCATION
        distances = []
        for stop in stops:
            distances.append(distanceBetween(currentLocation, stop, dtable))

        # NEXT STOP WILL BE THE CLOSEST ADDRESS OF ALL DROP OFF POINTS
        nextStop = stops[distances.index(min(distances))]

        # INCREASE TRUCK MILAGE
        distanceTravelled = distanceBetween(currentLocation, nextStop, dtable)
        truck.odometer+=distanceTravelled
        travelTime = calculateTime(distanceTravelled)
        currentTime = increaseTime(travelTime, currentTime)
        truck.clock = currentTime

        # "TRAVEL" TO THE NEXT STOP
        currentLocation = nextStop
        truck.location = currentLocation


        # DELIVER ALL PACKAGES AT THAT LOCATION
        for i in range(len(truck.cargo)):
            package = truck.cargo[i]
            if package is not None and package.addressID is currentLocation:
                package.status = Status.DELIVERED       # UPDATE DELIVERY STATUS
                package.deliveryTime = currentTime      # UPDATE DELIVERY TIME
                incrementCount()
                truck.locationHistory.append((package, currentLocation, package.deliveryTime))
                truck.cargo[i] = None

        # REMOVE CURRENT LOCATION FROM LIST OF STOPS
        stops.remove(currentLocation)
    
    # RETURN TO STATION
    truck.odometer+=(distanceBetween(currentLocation, startingLocation, dtable))
    distanceTravelled = distanceBetween(currentLocation, startingLocation, dtable)
    travelTime = calculateTime(distanceTravelled)
    currentTime = increaseTime(travelTime, currentTime)
    truck.clock = currentTime
    currentLocation = startingLocation
    truck.location = currentLocation
    truck.cargo = []    # EMPTY TRUCK CARGO LIST
        
def updatePackage9(package, table):
    table.delete(table.search(package))
    package.address = "410 S State St"
    package.city = "Salt Lake City"
    package.state = "UT"
    package.zip = 84111
    package.status = Status.AT_HUB
    package.addressID = 19
    table.insert(package)


    
def packageStats(time, packages):
    # FIGURES OUT WHERE THE PACKAGE IS AT THE CHOSEN TIME
    for package in packages:
        if package.departTime > time:
            # package still at hub
            print(f"Package: {package.id}\tStatus: AT_HUB")
        elif package.departTime < time and time < package.deliveryTime:
            # package en route
            print(f"Package: {package.id}\tStatus: EN_ROUTE")
        elif time > package.deliveryTime:
            # package delivered already
            print(f"Package: {package.id}\tStatus: DELIVERED\tDelivery Time: {package.deliveryTime}")

    pass

def printStats(trucklist):
    mileage = trucklist[0].odometer+trucklist[1].odometer+trucklist[2].odometer
    print(f"PACKAGES DELIVERED:\t{PACKAGES_DELIVERED}")
    print(f"TRUCK 1 ODOMETER:\t{trucklist[0].odometer}")
    print(f"TRUCK 2 ODOMETER:\t{trucklist[1].odometer}")
    print(f"TRUCK 3 ODOMETER:\t{trucklist[2].odometer}")
    print(f"TOTAL MILEAGE:\t\t{mileage}")

def main():
# IMPORT DATA FROM FILES
    packages = data.loadPackageData()
    addresses = data.loadAddressData()
    distanceTable = data.loadDistanceData()

# SET THE ADDRESSID FOR EACH PACKAGE. TO BE USED FOR HASH TABLE KEY
    for package in packages:
        for address in addresses:
            if package.address == address:
                package.addressID = addresses.index(address)
                break

# SETS DELAYED STATUS FOR DELAYED PACKAGES
    for package in packages:
        if "Delayed" in package.note or package.id == 9:
            package.status = Status.DELAYED

# CREATE HASH TABLE AND LOAD PACKAGES
    hashTable = HashTable(len(addresses))
    for package in packages:
        hashTable.insert(package)

# CREATE TRUCK OBJECTS
    Truck1 = Truck(1)
    Truck2 = Truck(2)
    Truck3 = Truck(3)
    TruckList = [Truck1, Truck2, Truck3]

# START AT 8:00
    currentTime = START_TIME
    
# MANUALLY LOAD TRUCKS ACCORDING TO RESTRICTIONS
    manualLoadRestricted(TruckList, packages, hashTable)

# PACKAGES LEFT IN HASH TABLE AT THIS POINT DO NOT HAVE A RESTRICTION OTHER THAN BEING DELAYED
# FILL THE EMPTY SPACE ON EACH TRUCK
    fillTruck(Truck1, hashTable)
    fillTruck(Truck2, hashTable)
    
# TRUCK 3 WILL WAIT TO BE LOADED UNTIL 9:05 AND WILL TAKE THE DELAYED PACKAGES

# DELIVER FIRST PACKAGES
# TRUCK 1 AND 2 LEAVE HUB AT 8:00
    # TRUCK.CLOCK WILL TRACK THE TIME OF DAY FOR EACH TRUCK
    deliverPackages(Truck1, distanceTable, Truck1.clock)
    deliverPackages(Truck2, distanceTable, Truck2.clock)
    # TRUCKS RETURN TO HUB AFTER DELIVERY
    
# TIME HITS 9:05 WHILE THEY ARE DELIVERING
# UPDATE DELAYED PACKAGES
    currentTime = time(9,5,0)
    for package in packages:
        if package.status is Status.DELAYED and package.id != 9:    # package 9 delayed until 10:25
            package.status = Status.AT_HUB

# LOAD TRUCK 3 WITH REMAINING PACKAGES
# ONLY PACKAGE 9 WILL BE LEFT IN HASHTABLE
    fillTruck(Truck3, hashTable)

# TRUCK 3 MUST WAIT FOR 1 OTHER TRUCK TO ARRIVE BACK AT HUB
    returnTimes = [Truck1.clock, Truck2.clock]
    firstBack = min(returnTimes)
    if firstBack < time(9,5,0):
        Truck3.clock = time(9,5,0)
    else:
        Truck3.clock = firstBack

# TRUCK 3 DEPARTS - ONLY TRUCK ON ROAD AT THIS POINT
    deliverPackages(Truck3, distanceTable, Truck3.clock)

# TIME HITS 10:25
# PACKAGE 9 GETS THE CORRECT ADDRESS
    currentTime = time(10,25,0)
    updatePackage9(packages[8], hashTable)

# FIGURE OUT WHICH TRUCK CAN TAKE LAST PACKAGE
    while hashTable.contents > 0:
        for truck in TruckList:
            if truck.clock <= time(10,25,0) and truck.location == 0:
                fillTruck(truck, hashTable)
                truck.clock = time(10,25,0)
                if truck.cargo:
                    deliverPackages(truck, distanceTable, truck.clock)
                    TIME_COMPLETED=truck.clock

# DISPLAY MENU
    while True:
        print("Make a selection: \n")
        print("1. Locate Single Package")
        print("2. Display All Package Info")
        print("3. Display statistics")
        print("4. QUIT")
        selection = int(input())
        if selection == 1:
            packageToSearch = input("Enter Package ID: ")
            print(packages[int(packageToSearch) - 1])
        elif selection == 2:
            t = input("Enter time in format HH:MM:SS: ")
            t = t.split(':')
            t = timedelta(hours=float(t[0]), minutes=float(t[1]), seconds=float(t[2]))
            t = (datetime.min + t).time()
            print(t)
            packageStats(t, packages)
        elif selection == 3:
            printStats(TruckList)
        elif selection == 4:
            quit()


if __name__ == "__main__":
    main()