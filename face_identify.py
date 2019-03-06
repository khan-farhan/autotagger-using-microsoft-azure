import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '*****************',
}

params = urllib.parse.urlencode({
})

body = {

    "personGroupId": "firstgroup",
    "faceIds": [
        "3fd80a22-b537-4ce4-8ffb-938b6156f5b8",
        "adfcec24-fbba-4066-9304-440a10b9afe0"
    ],
    "maxNumOfCandidatesReturned": 2,
    "confidenceThreshold": 0.5
}
try:
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/identify?%s" % params, str(body), headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
