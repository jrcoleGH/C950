
import csv
import datetime


# Class to create distance object and calculate all distance needs
class Distance:
    def __init__(self):
        # initialize address and distance lists
        self.address_data_list = []
        self.distance_data_list = []
        self.truck_miles = 0
        self.time_delivered = 0

    # load address data into list
    def loadAddressData(self, fileName):
        # open distance file and insert addresses into list
        with open(fileName) as address_data:
            addressData = csv.reader(address_data)
            # skip header
            for address in addressData:
                self.address_data_list.append(address[2])

    # load distance data into list
    def loadDistanceData(self, fileName):
        # open distance file and insert into distances into 2D list
        with open(fileName) as distance_data:
            distanceData = csv.reader(distance_data)
            # skip header
            next(distanceData)
            for distance in distanceData:
                self.distance_data_list.append(distance[1:])

    # finds distance between two addresses
    def distanceBetween(self, address1, address2):
        return self.distance_data_list[self.address_data_list.index(address1)][self.address_data_list.index(address2)]

    # returns address based on package ID
    def getAddress(self, p, key):
        return p.address_info[key]

    # calculates minimum distance between one address and all pkg addresses on truck
    # starts with Hub address when called for the first time
    # Nearest Neighbor Algorithm
    # O(n^2) Average Time Complexity
    def minDistanceFrom(self, d, p, truck, hashTable, addressFrom, truckPackages, currentTime):
        minimum = 1000.00
        current_address = addressFrom
        minimum_address = current_address
        pkg_to_deliver_next = 0
        # looping through packages on truck to compare distances
        for index in range(len(truckPackages)):
            pkgID = int(str(truckPackages[index]).split(", ")[0])
            next_address = d.getAddress(p, pkgID)
            a1_a2 = float(d.distanceBetween(current_address, next_address))
            # checks if distance to next address is less than distance from previous package
            if a1_a2 < minimum:
                minimum = a1_a2
                minimum_address = next_address
                pkg_to_deliver_next = pkgID
        # saves delivery time stamp based distance travelled
        self.time_delivered = d.timeDelivered(minimum)
        # marks package as delivered
        truck.isDelivered(p, pkg_to_deliver_next, hashTable, currentTime, self.time_delivered)
        return_values = [minimum_address, minimum]
        return return_values

    # method to return delivery time
    def timeDelivered(self, miles):
        seconds_to_drive = float((60 * 60) * (miles / 18))
        time_delivered = self.time_delivered + datetime.timedelta(0, seconds_to_drive)
        return time_delivered

    # method to initiate delivery of packages on truck
    # O(n) Average Time Complexity
    def deliverPackages(self, d, p, truck, hashTable, currentTime, startTime):
        self.time_delivered = startTime
        current_address = '4001 S 700 E'
        truck_delivering = truck.packages_on_truck
        total_miles_travelled = 0
        # loops through packages on truck until all are delivered based on minimum distance
        for packages in range(len(truck_delivering)):
            current_values = d.minDistanceFrom(d, p, truck, hashTable, current_address, truck_delivering,
                                               currentTime)
            current_address = current_values[0]
            current_min_distance = float(current_values[1])
            total_miles_travelled = total_miles_travelled + current_min_distance
        self.truck_miles = total_miles_travelled  # saves total miles driven by the truck
        return total_miles_travelled

