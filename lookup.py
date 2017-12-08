import flask
from flask_api import status

app = flask.Flask(__name__)

test = ['www.reddit.com/r/dailyprogrammer','www.stackoverflow.com/questions/41718376/how-to-unit-test-a-flask-restful-api']

# <hostname_and_port> <original_path_and_query_string>
# www.reddit.com:80 / r/dailyprogrammer

# this should give a 400
# http://127.0.0.1:5000/urlinfo/1/www.reddit.com:80/r/dailyprogrammer 
# this should redirect
# http://127.0.0.1:5000/urlinfo/1/www.reddit.com:80/r/programmerhumor

@app.route('/urlinfo/1/<hostname_and_port>/<path:original_path_and_query_string>', methods=['GET'])
def lookup(hostname_and_port, original_path_and_query_string):
    hostname, port = hostname_and_port.split(':')
    url = hostname + '/' + original_path_and_query_string
    if url in test:
        return 'malicious', status.HTTP_400_BAD_REQUEST
    resp = flask.make_response('')
    resp.headers['Location'] = 'http://' + url
    return resp, status.HTTP_302_FOUND

if __name__ == "__main__":
    app.run(debug=True)
