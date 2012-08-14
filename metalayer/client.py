"""
Simple client to the MetaLayer API.

Usage:

    import metalayer

    client = metalayer.Client()

    # Run sentiment analysis over a string
    client.data.sentiment("I love kittens")

    # Retrieve keywords from a string
    client.data.tagging("Kittens and puppies and bears")

    # Extract geographic information from a string
    client.data.locations("Puppies in Bozeman are the best")

    # Run the three preceding endpoints over a string in one shot
    client.data.bundle("The best kittens are from MT")

    # Extract color information from an image
    with open('/path/to/file', 'rb') as f:
        client.data.color(f)

    # Generate a histogram of color distribution from an image
    with open('/path/to/file', 'rb') as f:
        client.data.histogram(f)
"""

import json
import requests


class _Client(object):
    """Base client class, responsible for sending the HTTP request."""

    _layer = None

    def _send_request(self, endpoint, data=None, files=None):
        """Fire off the HTTP request and do some minimal processing to the
        response.
        """

        if files:
            [f.seek(0) for f in files.values()]

        url = "%s/%s/%d/%s" % (Client.HOST, self._layer, Client.VERSION,
            endpoint)
        response = requests.post(url, data=data, files=files)
        response = json.loads(response.text)

        if response['status'] != "success":
            raise Exception(". ".join(response['response']['errors']))

        return response['response']


class _Data(_Client):
    """Client for the data layer API."""

    _layer = "datalayer"

    def sentiment(self, text):
        """Sentiment analysis as performed by the text API returns a float
        value between -5.0 and 5.0 with 0 being neutral in tone (or no
        sentiment could be extracted), 5.0 being the happiest little piece of
        text in the world, and -5.0 being the kind of text that really should
        seek anger management counseling!
        """

        response = self._send_request("sentiment", dict(text=text))
        return response[self._layer]['sentiment']

    def tagging(self, text):
        """The tagging functions looks for the uncommon keywords in a text and
        uses the strongest keywords (with the help of natural language
        processing) to 'tag' content. This effectively allows you to
        algorithmically group content with related keywords together.
        """

        response = self._send_request("tagging", dict(text=text))
        return response[self._layer]['tags']

    def locations(self, text):
        """Location disambiguation is a technique that uses a series of clues
        to locate places an item of text might be referring to (or where the
        user creating the text is located). This is done using natural language
        processing where using meta data has failed to offer useful location
        data.
        """

        response = self._send_request("locations", dict(text=text))
        return response[self._layer]['locations']

    def bundle(self, text):
        """This call allows you to send one request to all three API functions
        (sentiment, tagging, and location). The response is neatly packaged
        JSON.
        """

        response = self._send_request("bundle", dict(text=text))
        return response[self._layer]


class _Image(_Client):
    """Client for the image layer API."""

    _layer = "imglayer"

    def color(self, image):
        """This request returns all the colors in an image as RGB values."""

        response = self._send_request("color", files=dict(image=image))
        return response[self._layer]['colors']

    def histogram(self, image):
        """In image processing, a color histogram is a representation of the
        distribution of colors in an image. Histogram is not to be confused
        with the Color function, in that it returns color samples and
        positioning (as opposed to only colors).
        """

        response = self._send_request("histogram", files=dict(image=image))
        return response[self._layer]['histogram']

    def ocr(self, image):
        """This API function allows users to make attempts to parse readable
        text from image documents. This might be used to improve visual search
        techniques or auto-categorize images when paired with the Tagging API
        function.
        """

        response = self._send_request("ocr", files=dict(image=image))
        return response[_Data._layer]

    def faces(self, image):
        """This function allows users to identify objects within photo
        documents and get back the positioning of those objects relative to the
        document. Currently the algorithm is trained to universally identify
        human faces, however it can be trained to recognize anything.
        """

        response = self._send_request("faces", files=dict(image=image))
        return response['objectdetection']

    def bundle(self, image):
        """This call allows you to send one request to all four API functions
        (color, histogram, OCR, and object detection). The response is neatly
        packaged JSON.
        """

        response = self._send_request("bundle", files=dict(image=image))
        return response[self._layer]


class Client(object):
    """Client to the MetaLayer API. This is strictly a convenience class which
    delegates functionality to the `_Client` class and its subclasses.

    Usage:
        client = Client()

        # Run sentiment analysis over a string
        client.data.sentiment("I love kittens")

        # Retrieve keywords from a string
        client.data.tagging("Kittens and puppies and bears")

        # Extract geographic information from a string
        client.data.locations("Puppies in Bozeman are the best")

        # Run the three preceding endpoints over a string in one shot
        client.data.bundle("The best kittens are from MT")

        # Extract color information from an image
        with open('/path/to/file', 'rb') as f:
            client.data.color(f)

        # Generate a histogram of color distribution from an image
        with open('/path/to/file', 'rb') as f:
            client.data.histogram(f)
    """

    HOST = "http://api.metalayer.com/s"
    VERSION = 1

    _layer_class_map = {
        "data": _Data,
        "image": _Image
    }

    def __init__(self):
        """Create instances of each available layer."""

        for layer in self._layer_class_map:
            setattr(self, layer, self._layer_class_map[layer]())
