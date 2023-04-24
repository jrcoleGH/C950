# Ref: C950 - Webinar-1 - Let’s Go Hashing
# Ref: C950 - Webinar-3 - How to Dijkstra

import csv


# Class to create Package object
# Ref: "C950 - Webinar-3 - How to Dijkstra"
class Package:
    def __init__(self, ID, address, city, state, zip, deadline, weight, notes, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status

    # overwrite print(Package) otherwise it will print object reference
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (
            self.ID, self.address, self.city, self.state, self.zip, self.deadline, self.weight, self.status)


# Class to create Hash table
class PkgHash:
    def __init__(self):
        # initialize the hash table with empty bucket list entries.
        self.pkg_data_table = []
        self.address_info = ["4001 S 700 E"]
        data = csv.reader(open('WGUPS_Package_File.csv', 'r'))
        for row in data:
            self.pkg_data_table.append([])

    # does both insert and update
    # get the bucket list where this item will go
    # O(1) Average Time Complexity for insert
    # Ref: "C950 - Webinar-1 - Let’s Go Hashing"
    def insert(self, key, item):
        pkg_bucket = hash(key) % len(self.pkg_data_table)
        pkg_bucket_list = self.pkg_data_table[pkg_bucket]

        # update key if it is already in the bucket
        for kv in pkg_bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # if not, insert the item to the end of the bucket list
        key_value = [key, item]
        pkg_bucket_list.append(key_value)
        return True

    # Searches for an item with matching key in the hash table
    # Returns the item if found, or None if not found
    # O(1) Average Time Complexity for lookup
    # Ref: "C950 - Webinar-1 - Let’s Go Hashing"
    def search(self, key, hashTable):
        # get the bucket list where this key would be
        pkg_bucket = hash(key) % len(hashTable)
        pkg_bucket_list = hashTable[pkg_bucket]

        # search for the key in the bucket list
        for kv in pkg_bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    # Removes an item with matching key from the hash table
    # Not used currently but would be used to reload info on a daily basis
    # O(1) Average Time Complexity for removal
    # Ref: "C950 - Webinar-1 - Let’s Go Hashing"
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        pkg_bucket = hash(key) % len(self.pkg_data_table)
        pkg_bucket_list = self.pkg_data_table[pkg_bucket]

        # remove the item from the bucket list if it is present
        for kv in pkg_bucket_list:
            if kv[0] == key:
                pkg_bucket_list.remove([kv[0], kv[1]])

    # method to load package date and create package objects
    # Ref: C950 - "Webinar-3 - How to Dijkstra"
    def loadPkgData(self, fileName, pHash):
        # open pkg file and insert into list
        with open(fileName) as pkg_data:
            pkgData = csv.reader(pkg_data)
            # skip header
            next(pkgData)
            for pkg in pkgData:
                pID = int(pkg[0])
                pAddress = pkg[1]
                pCity = pkg[2]
                pState = pkg[3]
                pZip = pkg[4]
                pDeadline = pkg[5]
                pWeight = pkg[6]
                pNotes = pkg[7]
                pStatus = "Package "
                # package object
                p = Package(pID, pAddress, pCity, pState, pZip, pDeadline, pWeight, pNotes, pStatus)
                # Hash table insertion
                pHash.insert(pID, p)
                self.address_info.append(pAddress)
        return self.pkg_data_table