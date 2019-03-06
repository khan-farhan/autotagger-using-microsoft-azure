import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '*****************',
}

params = urllib.parse.urlencode({
})


def train(persongroupID):

    try:
        print("Training the group ..")
        conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/persongroups/{0}".format(persongroupID) + "/train?%s" % params, "{}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("Error while training")
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
