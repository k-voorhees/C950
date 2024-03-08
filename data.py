import pandas as pd
import numpy as np
import math
from package import Package


def loadPackageData():
    # create datafrom
    data = pd.read_excel("./package_file.xlsx", skiprows=7)

    # rename columns - easier to work with
    data = data.rename(columns={"Package\nID" : "PackageID", "Delivery\nDeadline" : "Deadline", "Weight\nKILO":"Weight", "page 1 of 1PageSpecial Notes" : "Special Notes"}, errors="raise")


    # replaces Nan in special note with empty string
    data = data.replace(np.nan, "")

    # create packageList
    packages = []

    # adds each row to the packageList
    for row in data.itertuples(index=False):
        packages.append(Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    return packages

def loadAddressData():
    # returns a list of tuples of (address, index)
    data = pd.read_excel('./distance_table.xlsx', skiprows=7)

    addressData = []

    for row in data.itertuples():
        addressData.append(row[1].split("\n")[1].strip())
    return addressData

def loadDistanceData():
    # returns a distance matrix
    data = pd.read_excel('./distance_table.xlsx', skiprows=7)

    addressData = loadAddressData()

    matrix_length = len(addressData)
    matrix = [] * matrix_length

    for row in data.itertuples():
        a = []
        for col in range(3,30):
            a.append(float(row[col]))
        matrix.append(a)

    for row in range(matrix_length):
        for col in range(matrix_length):
            if math.isnan(matrix[row][col]):
                matrix[row][col] = matrix[col][row]

    # ***********
    # print function to display matrix
    # ***********
                
    # for row in range(matrix_length):
    #     for col in range(matrix_length):
    #         print(str(matrix[row][col])+ "\t", end=" ")
    #     print()

    return matrix