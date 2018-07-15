import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64
import cv2
import pandas as pd
import os

database_path = os.getcwd() + "/Database.csv"


def capture(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)
            img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imshow('my webcam', img)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()

    return img1


def name_to_ID(persongroupID, person_name):
    df = pd.read_csv(database_path)
    personID = df.loc[(df['personName'] == person_name) & (df['persongroupID'] == persongroupID), 'personId'].iloc[0]
    return personID


headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '*****************',
}


params = urllib.parse.urlencode({})


def add_face(persongroupID):

    print("Capturing Image ...")
    person_name = input("Enter the name of the person whose face is to be added: ")
    personID = name_to_ID(persongroupID, person_name)
    img = capture(mirror=True)
    img_str = cv2.imencode('.jpg', img)[1].tostring()

    try:
        conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        personID = name_to_ID(persongroupID, person_name)
        conn.request("POST", "/face/v1.0/persongroups/{0}/persons/{1}/persistedFaces".format(persongroupID, personID) + "?%s" % params, img_str, headers)
        response = conn.getresponse()
        data = response.read()
        print("Face added Successfully")
        # print(data)
        conn.close()
    except Exception as e:
        print("Error while adding face")
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


if __name__ == '__main__':
    persongroupID = input("Enter group ID: ")
    add_face(persongroupID)
