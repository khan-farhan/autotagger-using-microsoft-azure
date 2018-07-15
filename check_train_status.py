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


def check_status(persongroupID):

    try:
        print("Checking training status ..")
        conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("GET", "/face/v1.0/persongroups/{0}".format(persongroupID) + "/training?%s" % params, "{}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("Error while checking status")
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
