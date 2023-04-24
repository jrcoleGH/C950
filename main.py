# Jennifer Cole - Student ID: 001265274
# Main method and user prompts

from package import PkgHash
from distance import Distance
from truck import Truck
from datetime import datetime

now = datetime.now()
eightAM = now.replace(hour=8, minute=0, second=0, microsecond=0)
nineZeroFiveAM = now.replace(hour=9, minute=5, second=30, microsecond=0)
tenAM = now.replace(hour=10, minute=0, second=0, microsecond=0)


# method to get input for current time
def user_prompt_time():
    user_input_time = (input('Input current time as 24 hour format. '
                             'Example 8:32 (for 8:32am) or 15:30 (for 3:30pm) etc: '))
    hour = int(user_input_time.split(":")[0])
    minute = int(user_input_time.split(":")[1])
    current_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    return current_time


# method to get input for user choice
def user_prompt(hashTable):
    # checking for user input and throwing exception if not a number
    while True:
        try:
            user_input = int(input('Enter 1 to search for a single package or 2 to get the status of all packages: '))
            check_input(user_input, hashTable)
            break;
        except ValueError:
            print("Invalid input")


# checking if input number is a 1 or 2
def check_input(user_input, hashTable):
    p = PkgHash()
    if user_input == 1:
        pkg_ID_input = int(input('Enter package ID: '))
        # search hashtable for package ID
        kv = p.search(pkg_ID_input, hashTable)
        if kv is None:
            print("Package ID does not exist")
        else:
            print(p.search(pkg_ID_input, hashTable))
    elif user_input == 2:
        # print status of all packages
        print('Status of all packages:')
        for i in range(len(p.pkg_data_table) - 1):
            print("Package ID: {}".format(p.search((i + 1), hashTable)))
    else:
        print('Try again. ')
        user_prompt(hashTable)

    input('Press Enter to exit command prompt.')


# Main method to start program
def main():
    current_time = user_prompt_time()
    p = PkgHash()  # creating new PkHash object
    d = Distance()
    hashTable = p.loadPkgData('WGUPS_Package_File.csv', p)
    d.loadAddressData('WGUPS_Address_File.csv')
    d.loadDistanceData('WGUPS_Distance_Table.csv')
    # manually choosing which packages go on each truck
    t1packages = [1, 9, 13, 14, 15, 19, 16, 20, 29, 30, 31, 34, 37, 40]  # early deliveries, leave at 8am
    t2packages = [3, 18, 36, 38, 5, 8, 11, 12, 23, 27, 35, 39]  # eod pkgs, leave when truck 1 comes back at 10am
    t3packages = [6, 25, 2, 4, 7, 10, 17, 21, 22, 24, 26, 28, 32, 33]  # closet eod and late arrival, leave at 9:10
    # creating truck objects and loading all 3 trucks
    truck1 = Truck()
    truck1.loadTruck(t1packages, p, hashTable)
    truck2 = Truck()
    truck2.loadTruck(t2packages, p, hashTable)
    truck3 = Truck()
    truck3.loadTruck(t3packages, p, hashTable)
    # delivering packages on each truck
    truck1miles = d.deliverPackages(d, p, truck1, hashTable, current_time, eightAM)
    truck2miles = d.deliverPackages(d, p, truck2, hashTable, current_time, tenAM)
    truck3miles = d.deliverPackages(d, p, truck3, hashTable, current_time, nineZeroFiveAM)
    totalMiles = truck1miles + truck2miles + truck3miles  # adding miles driven by each truck
    print("Total Miles Driven BY All Trucks")
    print(totalMiles)
    user_prompt(hashTable)


if __name__ == '__main__':
    main()
