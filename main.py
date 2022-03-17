# Daniel Cunningham
# Student ID #001197223

import csv
import datetime

# Hash Table class
class HashTable(object):
    def __init__(self, length):
        self.array = [None] * length

    def hash(self, key):
        length = len(self.array)
        return key % length

    def insert(self, key, value):
        index = self.hash(key)
        if self.array[index] is not None:
            self.array[index][0][0] = key
            self.array[index][0][1] = value
        else:
            self.array[index] = []
            self.array[index].append([key, value])

    def lookup(self, key):
        index = self.hash(key)
        if self.array[index] is None or self.array[index][0][0] != key:
            return "this key does not exist"
        else:
            return self.array[index][0][1]

    def length(self):
        return len(self.array)

# Package class
class Package(object):
    def __init__(self, id, address, city, state, zipCode, deadline, weight, notes):
        self.id = id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.state = state
        self.zipCode = zipCode
        self.weight = weight
        self.notes = notes
        self.timeDelivered = ""
        self.leftHub = ""
        self.status = "at the hub"
        self.truck = ""

    def getId(self):
        return int(self.id)

    def getAddress(self):
        return self.address.split()

    def getNotes(self):
        return self.notes

    def getDeadline(self):
        return self.deadline

    def setTimeDelivered(self, timeDelivered):
        self.timeDelivered = timeDelivered

    def setLeftHub(self, leftHub):
        self.leftHub = leftHub

    def setStatus(self, status):
        self.status = status

    def setTruck(self, truck):
        self.truck = truck

    def __str__(self):
        if self.leftHub != "" and self.timeDelivered == "":
            return "Package ID: "+ self.id + ", Address: " + self.address + ", Deadline: " + self.deadline + \
                ", Status: " + self.status + ", Truck: " + self.truck + ", Notes: " + self.notes + ", Left Hub: " + self.leftHub
        elif self.timeDelivered != "":
            return "Package ID: " + self.id + ", Address: " + self.address + ", Deadline: " + self.deadline + \
                ", Status: " + self.status + ", Truck: " + self.truck + ", Notes: " + self.notes + ", Left Hub: " + \
                self.leftHub + ", Delivered: " + self.timeDelivered
        else:
            return "Package ID: "+ self.id + ", Address: " + self.address + ", Deadline: " + self.deadline + \
                ", Status: " + self.status + ", Notes: " + self.notes

# function that returns the number associated with an address
def addressLookup(address):
    return addresses.index(address)

# function that returns the distance between the 2 given addresses
def distanceBetween(address1, address2):
    if distances[addressLookup(address1)][addressLookup(address2)] != '':
        return distances[addressLookup(address1)][addressLookup(address2)]
    else:
        return distances[addressLookup(address2)][addressLookup(address1)]

# function the checks the packages on the truck and returns the one with the
# closest address to the current address
# this function has a time complexity of O(n)
def minDistanceFrom(fromAddress, truckPackages):
    min = None
    closest = None
    for i in truckPackages:
        if min != None:
            if distanceBetween(fromAddress, i.getAddress()) < min:
                min = distanceBetween(fromAddress, i.getAddress())
                closest = i
        else:
            min = distanceBetween(fromAddress, i.getAddress())
            closest = i
    return closest

# function for loading the trucks
# this function has a time complexity of O(n)
def loadTrucks(truck1, truck2, truck3):
    count1 = 1
    count2 = 0
    remaining = []
    for i in range(1, packages.length() + 1):
        if packages.lookup(i).getNotes() == 'Can only be on truck 2':
            packages.lookup(i).setTruck("#2")
            truck2.append(packages.lookup(i))
        elif packages.lookup(i).getNotes() == 'Delayed on flight---will not arrive to depot until 9:05 am':
            packages.lookup(i).setTruck("#2")
            truck2.append(packages.lookup(i))
        elif packages.lookup(i).getNotes() == 'Wrong address listed':
            packages.lookup(i).setTruck("#3")
            truck3.append(packages.lookup(i))
        elif packages.lookup(i).getId() in (13, 14, 15, 16, 19, 20):
            packages.lookup(i).setTruck("#1")
            truck1.append(packages.lookup(i))
        elif packages.lookup(i).getDeadline() != 'EOD' and count1 < 5:
            packages.lookup(i).setTruck("#1")
            truck1.append(packages.lookup(i))
            count1 += 1
        elif packages.lookup(i).getDeadline() != 'EOD' and count2 < 5:
            packages.lookup(i).setTruck("#2")
            truck2.append(packages.lookup(i))
            count2 += 1
        else:
            remaining.append(packages.lookup(i))
    for j in range(0, len(remaining)):
        if len(truck1) < 10:
            remaining[j].setTruck("#1")
            truck1.append(remaining[j])
        elif len(truck2) < 16:
            remaining[j].setTruck("#2")
            truck2.append(remaining[j])
        else:
            remaining[j].setTruck("#3")
            truck3.append(remaining[j])

# function for delivering the packages, this is the main algorithm
# this function has a time complexity of O(n^2)
def deliverPackages(truck, startTime, endTime):
    time = startTime
    distance = 0
    currentAdd = addresses[0]
    priority = []
    for i in truck:
        if time < endTime:
            i.setStatus("en route")
            i.setLeftHub(time.time().strftime("%H:%M"))
        if i.getDeadline() != 'EOD':
            priority.append(i)
    while len(priority) > 0 and time < endTime:
        next = minDistanceFrom(currentAdd, priority)
        nextDistance = distanceBetween(currentAdd, next.getAddress())
        time += datetime.timedelta(hours = (nextDistance/18))
        if time > endTime:
            break
        distance += nextDistance
        currentAdd = next.getAddress()
        next.setTimeDelivered(time.time().strftime("%H:%M"))
        next.setStatus("delivered")
        packages.insert(next.getId(), next)
        priority.remove(next)
        truck.remove(next)
    while len(truck) > 0 and time < endTime:
        next = minDistanceFrom(currentAdd, truck)
        nextDistance = distanceBetween(currentAdd, next.getAddress())
        time += datetime.timedelta(hours=(nextDistance / 18))
        if time > endTime:
            break
        distance += nextDistance
        currentAdd = next.getAddress()
        next.setTimeDelivered(time.time().strftime("%H:%M"))
        next.setStatus("delivered")
        packages.insert(next.getId(), next)
        truck.remove(next)
    distance += distanceBetween(currentAdd, addresses[0])
    return distance

# Create 'packages' hash table
packages = HashTable(40)
# load packages into 'packages' from CSV file
with open('Package File CSV.csv') as packFile:
    readPackFile = csv.reader(packFile, delimiter = ',')
    for row in readPackFile:
        if len(row) > 1:
            package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            packages.insert(package.getId(), package)

# create 'distance' list which will be a list of lists
distances = []
# load distance data into distance list
with open('Distances.csv') as distFile:
    readDistFile = csv.reader(distFile, delimiter = ',')
    for row in readDistFile:
        arr = []
        for num in row:
            if num != '':
                arr.append(float(num))
            else:
                arr.append(num)
        distances.append(arr)

# create list to store addresses and assign them numbers
addresses = []
# load addresses in to addresses list
with open('Addresses.csv') as addFile:
    readAddFile = csv.reader(addFile)
    for row in addFile:
        addresses.append(str(row).split())

# create delivery trucks as lists that will hold packages
truck1 = []
truck2 = []
truck3 = []
# call function to load the trucks heuristically
loadTrucks(truck1, truck2, truck3)
# display number of packages in each truck
print('\ntruck1 - ', len(truck1), ' packages')
print('truck2 - ', len(truck2), ' packages')
print('truck3 - ', len(truck3), ' packages\n')

# input time at which user would like to check packages
time = input("Enter a time after 8:00AM in military time (i.e. 9:00AM would be" +
             " 0900): ")
# user input time, used to stop the algorithm at the correct time to display packages at that time
endTime = datetime.datetime(100, 1, 1, int(time[0:2]), int(time[2:4]))
# Truck 1 start time
startTime1 = datetime.datetime(100, 1, 1, 8, 0)
# Truck 2 start time
startTime2 = datetime.datetime(100, 1, 1, 9, 5)

# call deliverPackages for each truck and save the distance traveled
truck1Dist = deliverPackages(truck1, startTime1, endTime)
truck2Dist = deliverPackages(truck2, startTime2, endTime)
# truck 3 will not be able to leave the hub until truck 1 has returned
startTime3 = startTime1 + datetime.timedelta(hours = (truck1Dist / 18))
truck3Dist = deliverPackages(truck3, startTime3, endTime)

# display the total distance traveled by all 3 trucks
print('\nTotal distance traveled: ', truck1Dist + truck2Dist + truck3Dist, '\n')

# display all packages to the user
for i in range(1, 41):
    print(str(packages.lookup(i)))
