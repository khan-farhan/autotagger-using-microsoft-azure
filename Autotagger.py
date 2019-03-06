
"""
Person group ID needs to be provided. Run the script as python3 Autotagger.py groupID
Subscription key and Endpoint URI
"""

from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
from PIL import ImageDraw
import requests
import cv2
import numpy as np
import os
import pandas as pd
import sys

database_path = os.getcwd() + "/Database.csv"


def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))


def getFaceIDs(facelist):
    IDlist = []
    faceIDdictionary = {}
    for faceDictionary in facelist:
        IDlist.append(faceDictionary['faceId'])
    faceIDdictionary['faceIds'] = IDlist
    return faceIDdictionary


def rescaleCoordinates(oldRes, newRes, coord):
    newx1 = int(newRes[0] * (coord[0][0] / oldRes[1]))
    newx2 = int(newRes[1] * (coord[1][0] / oldRes[1]))

    newy1 = int(newRes[0] * (coord[0][1] / oldRes[0]))
    newy2 = int(newRes[1] * (coord[1][1] / oldRes[0]))

    return ((newx1, newy1), (newx2, newy2))


def ID_2_name(personGroupId, personId):
    df = pd.read_csv(database_path)
    person_name = df.loc[(df['personId'] == personId) & (df['persongroupID'] == personGroupId), 'personName'].iloc[0]
    return person_name


def faceapi(path):

    if len(path) > 0:

        global panelA
        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        oldRes = image.shape
        newRes = (800, 800)

        img_str = cv2.imencode('.jpg', image)[1].tostring()

        response = requests.post(uri_base + path_to_face_api,
                                 data=img_str,
                                 headers=face_detect_headers,
                                 params=params)

        faces = response.json()
        print(faces)

        face_identify_body = getFaceIDs(faces)
        face_identify_body["personGroupId"] = str(sys.argv[1])
        face_identify_body["maxNumOfCandidatesReturned"] = 1
        face_identify_body["confidenceThreshold"] = 0.5

        response = requests.post(uri_base + path_to_face_identify_api,
                                 data=str(face_identify_body),
                                 headers=face_identify_headers,
                                 params={})

        data = response.json()

        print(data)
        image = cv2.resize(image, newRes)

        for facedetectList, faceidentifyList in zip(faces, data):
            coordinates = getRectangle(facedetectList)
            newCoordinates = rescaleCoordinates(oldRes, newRes, coordinates)

            if len(faceidentifyList['candidates']) > 0:
                person_name = ID_2_name(face_identify_body["personGroupId"], faceidentifyList['candidates'][0]['personId'])
                cv2.putText(image, "Name: " + person_name, tuple(np.subtract(newCoordinates[0], (0, 18))), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, "confidence: " + str(faceidentifyList['candidates'][0]['confidence']), tuple(np.subtract(newCoordinates[0], (0, 6))), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.rectangle(image, newCoordinates[0], newCoordinates[1], (0, 255, 0), 3)

        image = Image.fromarray(image)

        image = ImageTk.PhotoImage(image)

        if panelA is None:

            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(padx=10, pady=10)

        else:

            panelA.configure(image=image)
            panelA.image = image


def select_image():

    path = filedialog.askopenfilename()

    faceapi(path)


subscription_key = '*****************',
uri_base = 'https://westcentralus.api.cognitive.microsoft.com'
path_to_face_api = '/face/v1.0/detect'
path_to_face_identify_api = "/face/v1.0/identify"
font = cv2.FONT_HERSHEY_SIMPLEX

face_detect_headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

face_identify_headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

params = {
    'returnFaceId': 'true',
}


if __name__ == '__main__':
    root = Tk()
    root.title("Face Detection")
    root.geometry("800x800")
    panelA = None

    btn = Button(master=root, text="Select an image", command=select_image)
    btn.pack(side="bottom", fill="both", expand="no", padx="10", pady="10")

    root.mainloop()
