"""
Adds a person to the group whose group id is given. It returns person's name and its unique ID which is generated by the api.
"""

import pandas as pd
import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64
import json
import os

database_path = os.getcwd() + "/Database.csv"


headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '1063e51066b4401984f1c6faeb40543e',
}

params = urllib.parse.urlencode({
})


def add_entry(persongroupID, personId, person_name):

    if not os.path.isfile(database_path):
        df = pd.DataFrame(columns=["persongroupID", "personId", "personName"])
        df.to_csv(database_path, index=False)

    df = pd.read_csv(database_path)
    labels = ["persongroupID", "personId", "personName"]
    df1 = pd.DataFrame.from_records([(persongroupID, personId, person_name)], columns=labels)
    df = df.append(df1, ignore_index=False)
    df.to_csv(database_path, index=False)


def add_person(persongroupID):
    print("Adding person to group ...")
    person_name = input("Enter the name of the person: ")

    try:
        conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/persongroups/" + "{0}".format(persongroupID) + "/persons?%s" % params, str({"name": "{0}".format(person_name)}), headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        # print(data)
        json_obj = json.loads(data)
        persondetails = {}
        persondetails['persongroupID'] = persongroupID
        persondetails['personId'] = json_obj['personId']
        persondetails['personName'] = person_name
        add_entry(persongroupID, json_obj['personId'], person_name)
        print("Person added successfully!")
        print(persondetails)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        print("Error in adding person")

    return persondetails


if __name__ == '__main__':
    persongroupID = input("Enter group ID: ")
    add_person(persongroupID)
