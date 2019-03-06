"""
Creates a person Group with the name and ID provided. 
"""


import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64
import json

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '1063e51066b4401984f1c6faeb40543e',
}

params = urllib.parse.urlencode({
})


def Group_create():

    print("Creating Group ...")
    persongroupID = input("Enter the group ID: ")
    GroupName = input("Enter name of the group: ")

    try:
        conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("PUT", "/face/v1.0/persongroups/" + "{0}".format(persongroupID) + "?%s" % params, str({"name": "{0}".format(GroupName)}), headers)
        response = conn.getresponse()
        data = response.read()
        groupDetails = {}
        groupDetails['GroupID'] = persongroupID
        groupDetails['GroupName'] = GroupName
        print(data)
        print("Group Creation is done!")
        print(groupDetails)
        conn.close()
    except Exception as e:
        print("Error in group Creation!")
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    return persongroupID, GroupName


if __name__ == '__main__':

    persongroupID, GroupName = Group_create()
