from random import randrange, choice
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
import json
from faker import Faker
fake = Faker()


def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

    
class Employee:
    def __init__(self, name, employeeId):
        self.name = name
        self.employeeId = employeeId

    def about(self):
        print("Name: {}\n ID: {}\n".format(self.name, self.employeeId))

class Deal:
    def __init__(self, dealId, status, dealerContacts, vehicleType, timeOfDeal):
        self.dealId = dealId,
        self.status = status,
        self.dealerContacts = dealerContacts
        self.vehicleType = vehicleType
        self.timeOfDeal = timeOfDeal

    def about(self):
        print("Deal ID: {}\n Deal Status: {}\n Employees on Deal: {}\n Vehicle Type: {}\n Time of Deal: {}".format(
            self.dealId, self.status, self.dealerContacts, self.vehicleType, self.timeOfDeal))

    def toJson(self):
            return json.dumps(self, default=lambda o: o.__dict__, 
                sort_keys=True, indent=4)



def generateEmployees(numberToGenerate: int):
    """ returns a list of randomly generated employees (name, employeeId) """
    # generate Employee list based on names and give unique employeeId
    employeeNameList = set()
    employeeIdList = set()
    employeeList = []

    for _ in range(numberToGenerate):
        employeeId = str(fake.msisdn())[0:6]
        while (employeeId in employeeIdList):
            employeeId = str(fake.msisdn())[0:6]
        employeeIdList.add(employeeId)

        employeeName = fake.name()
        while (employeeName in employeeNameList):
            employeeName = fake.name()
        employeeNameList.add(employeeName)
        employeeList.append(Employee(employeeName, employeeId))
    return employeeList


def generateDeals(numberToGenerate: int, employeeList: list):
    """ returns a list of randomly generated deals involving employees on the employeeList """
    statusList = ["CLEARED", "IN PROGRESS"]
    jobRoleList = ["SALESPERSON", "SALESMANAGER"]
    vehicleTypeList = ["NEW", "USED"]
    # generate Deal list and give unique employeeId
    dealList = []
    dealIdList = set()
    for _ in range(numberToGenerate):
        # grab 2 random employeeId
        dealEmployeeList = []
        employeeId1 = choice(employeeList).employeeId
        employeeId2 = choice(employeeList).employeeId
        while (employeeId1 == employeeId2):
            employeeId2 = choice(employeeList).employeeId
        dealEmployeeList.append(employeeId1)
        dealEmployeeList.append(employeeId2)
        # generate a unique random dealId
        dealId = str(fake.msisdn())[0:9]
        while (dealId in dealIdList):
            dealId = str(fake.msisdn())[0:9]
        dealIdList.add(dealId)
        # generate data for dealerContacts
        dealerContacts = []
        for idx, employeeId in enumerate(dealEmployeeList):
            employeeDealDict = dict()
            employeeDealDict["jobRole"] = "SALESMANAGER" if (
                idx == 0) else "SALESPERSON"
            employeeDealDict["employeeId"] = employeeId
            dealerContacts.append(employeeDealDict)

        # generate random date for deal in format --> 2018-02-20T14:30:00Z
        threeMonthsAgoDate = datetime.today() + relativedelta(months=-3)
        todayDate = datetime.today()
        randomDate = (random_date(threeMonthsAgoDate, todayDate).strftime('%Y-%m-%dT%H:%M:%SZ'))
        # create Deal and append to list
        dealList.append(Deal(dealId, choice(statusList), dealerContacts, choice(vehicleTypeList), randomDate))
    return dealList

if __name__ == "__main__":
    randomUniqueEmployees=generateEmployees(50)
    generatedDeals = generateDeals(15000, randomUniqueEmployees)

    # dump data to file
    # https://blog.softhints.com/python-convert-object-to-json-3-examples/
    with open("testData.json", "w") as write_file:
        itemsDict = dict()
        itemsDict["totalItems"] = 0
        itemsDict["items"] = []
        for deal in generatedDeals:
            itemsDict["totalItems"] += 1
            itemsDict["items"].append(
                    {
                        "dealId": deal.dealId,
                        "status": deal.status,
                        "orderInformation": {
                            "handover": {
                                "deliveryDate": deal.timeOfDeal
                            },
                            "dealerContacts": deal.dealerContacts
                        }
                    }
            )
        json.dump(itemsDict, write_file, indent=2)

# generate fake Deals API response as follows, all of these are inside of JSON object
# totalItems                                     --> number of deals
# items.dealId                                   --> id of specific deal
# items.status                                   --> status of deal, only need CLEARED
# items.dealerContacts.jobRole                   --> needs to be SALESPERSON
# items.dealerContacts.employeeId                --> is the employeeId
# items.vehicle.type                             --> "USED" or "NEW"
# items.orderInformation.handOver.deliveryDate   --> "2018-02-20T14:30:00Z"

# FOR EXAMPLE:

# {
#     "totalItems": 2,
#     "items": [
#         {
#             "dealId": "test123",
#             "status": "CLEARED",
#              "orderInformation": {
#                  "handOver": {
#                      "deliveryDate": "2018-02-20T14:30:00Z"
#                  },
#             "dealerContacts": [
#                     {
#                         "jobRole": "SALESPERSON",
#                         "employeeId": "joeb"
#                     },
#                     {
#                         "jobRole": "SALESMANAGER",
#                         "employeeId": "jeans"
#                     }
#                 ]
#         }
# }
