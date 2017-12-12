import flask
from flask_api import status

import redis

app = flask.Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# <hostname_and_port> <original_path_and_query_string>
# www.reddit.com:80 / r/dailyprogrammer

# this should give a 400
# http://127.0.0.1:5000/urlinfo/1/www.reddit.com:80/r/dailyprogrammer 
# this should redirect
# http://127.0.0.1:5000/urlinfo/1/www.reddit.com:80/r/programmerhumor

@app.route('/urlinfo/1/<hostname_and_port>/', defaults={'original_path_and_query_string': ''}, methods=['GET'])
@app.route('/urlinfo/1/<hostname_and_port>/<path:original_path_and_query_string>', methods=['GET'])
def lookup(hostname_and_port, original_path_and_query_string):
    hostname, port = hostname_and_port.split(':')
    url = hostname + ':' + port + '/' + original_path_and_query_string

    try:
        result = r.get(url)
    except:
        return 'service is down', status.HTTP_503_SERVICE_UNAVAILABLE

    if result is None:
        resp = flask.make_response('')
        resp.headers['Location'] = 'http://' + url
        return resp, status.HTTP_302_FOUND

    return 'malicious', status.HTTP_400_BAD_REQUEST

@app.route('/urlinfo/1/<hostname_and_port>/', defaults={'original_path_and_query_string': ''}, methods=['POST'])
@app.route('/urlinfo/1/<hostname_and_port>/<path:original_path_and_query_string>', methods=['POST'])
def add_url(hostname_and_port, original_path_and_query_string):
    hostname, port = hostname_and_port.split(':')
    url = hostname + ':' + port + '/' + original_path_and_query_string

    try:
        result = r.set(url,1)
    except:
        return 'service is down', status.HTTP_503_SERVICE_UNAVAILABLE

    if result is None:
        return 'could not update DB', status.HTTP_400_BAD_REQUEST

    return '', status.HTTP_200_OK

if __name__ == "__main__":
    app.run(debug=True)
