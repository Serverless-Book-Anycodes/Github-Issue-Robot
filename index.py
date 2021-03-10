import json
import uuid
import urllib.request

# Response
class Response:
    def __init__(self, start_response, response, errorCode=None):
        self.start = start_response
        responseBody = {
            'Error': {"Code": errorCode, "Message": response},
        } if errorCode else {
            'Response': response
        }
        # 默认增加uuid，便于后期定位
        responseBody['ResponseId'] = str(uuid.uuid1())
        print("Response: ", json.dumps(responseBody))
        self.response = json.dumps(responseBody)

    def __iter__(self):
        status = '200'
        response_headers = [('Content-type', 'application/json; charset=UTF-8')]
        self.start(status, response_headers)
        yield self.response.encode("utf-8")


def handler(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    requestBody = json.loads(environ['wsgi.input'].read(request_body_size).decode("utf-8"))

    responseData = "not issue opened"

    if requestBody['action'] == 'opened':
        print("title: ", requestBody['issue']['title'])
        print("url  : ", requestBody['issue']['url'])
        print("body : ", requestBody['issue']['body'])

        url = "https://"
        headers = {
          "Content-Type": "application/json"
        }
        urllib.request.urlopen(urllib.request.Request(url, json.dumps({
            "msgtype": "text",
            "text": {
                "content": "body"
            }
        }).encode("utf-8"), headers=headers))

        responseData = "issue opened"

    return Response(start_response, {"result": responseData})