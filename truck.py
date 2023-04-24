from datetime import datetime


# Class to create Truck object, passing package object(s) to that truck?
class Truck:
    def __init__(self):
        self.packages_on_truck = []

    # method to load packages on truck
    def loadTruck(self, packageList, pkg, hashTable):
        # gets package object from package ID and loads to truck
        for index in packageList:
            package = pkg.search(index, hashTable)
            self.packages_on_truck.append(package)

    # method to remove package from truck and updates hashtable with status
    def isDelivered(self, p, packageID, hashTable, currentTime, timeDelivered):
        now = datetime.now()
        eightAM = now.replace(hour=8, minute=0, second=0, microsecond=0)  # start of delivery day
        delivered = timeDelivered.strftime("%H:%M:%S")
        self.packages_on_truck.remove(p.search(packageID, hashTable))
        pkg_str = format(p.search(packageID, hashTable))  # package object in string format
        message1 = pkg_str + "is at the Hub"
        message2 = pkg_str + "is enRoute"
        message3 = pkg_str + "was delivered at: " + delivered
        # updates package status based on current time and delivery status
        if currentTime < eightAM:
            p.insert(packageID, message1)
        elif currentTime < timeDelivered:
            p.insert(packageID, message2)
        elif currentTime > timeDelivered:
            p.insert(packageID, message3)

