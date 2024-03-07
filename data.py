import pandas as pd
import numpy as np
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