from flask import Flask

import zmq
import logging

logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)

try:
    zmq_context = zmq.Context()
    socket_remote = zmq_context.socket(zmq.REQ)
    socket_remote.connect("tcp://zmq-server-service:55555")
except Exception as e:
    logging.error("[FLASK] Socket init failure")
    logging.error(e)


@app.route("/")
def hello_world():
    try:
        logging.debug("[FLASK /] Sending request")
        socket_remote.send_string(f"Request from flask.zmq.client.service to zmq.server.service")
        response = socket_remote.recv_string()
        logging.debug(f"[FLASK /] Received response '{response}'")
        return response
    except Exception as e:
        logging.error(e)


