"""
Websocket server for the browser plugin. Connects to the Mirametrix eye tracking server.

A thread is spawned for each client. The handler reads the xml stream and parses it on the fly.
Serializes the parsed objects to json and streams them to the client.

Author: Jiri Hamberg (jiri.hamberg@cs.helsinki.fi)
"""

import tornado.ioloop
import tornado.web
import tornado.websocket as websocket

import time, argparse, socket, sys, threading

import config
import xml_parser as parser


def request_data(sock, args):
    sock.send(str.encode( 
        '''<SET ID="ENABLE_SEND_POG_FIX" STATE="1" />\r\n
        <SET ID="ENABLE_SEND_EYE_LEFT" STATE="1" />\r\n
        <SET ID="ENABLE_SEND_EYE_RIGHT" STATE="1" />\r\n
        <SET ID="ENABLE_SEND_DATA" STATE="1" />\r\n'''
    ))

def get_xml_event_stream(args):
    """
    Get xml event stream from the eye tracking server or from a file.
    """
    if args.fake_eye_tracking:
        try:
            eye_tracking_stream = open(args.fake_eye_tracking)
        except IOError as e:
            print >> sys.stderr, "Could not open file: %s" % (e.strerror)
            exit(1)
    else:
        tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcpCliSock.connect((config.EYE_TRACKING_HOST, config.EYE_TRACKING_PORT))
            request_data(tcpCliSock, args)
        except socket.error as e:
            print >> sys.stderr, "Could not connect to eye tracking server: %s" % (e.strerror)
            sys.exit(1)
        eye_tracking_stream = tcpCliSock.makefile()
    return eye_tracking_stream

def handle_connection(connection, args):
    xml_event_stream = get_xml_event_stream(args)
    for event in parser.make_gaze_event_stream(xml_event_stream):
        message = event.json_encode()
        connection.write_message(message)

def main(args):
    class MirametrixWebSocketServer(websocket.WebSocketHandler):
        def check_origin(self, origin):
            return True
        def open(self):
            handler_thread = threading.Thread(target = handle_connection, args=(self, args))
            handler_thread.setDaemon(True)
            handler_thread.start()
        def on_message(self, message):
            pass
        def on_close(self):
            pass
    
    print "Starting websocket server on localhost:%s" % (config.BACKEND_PORT)
    app = tornado.web.Application([
        (r'/', MirametrixWebSocketServer)
    ])
        
    app.listen(config.BACKEND_PORT)
    tornado.ioloop.IOLoop.instance().start()
    
if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--fake-eye-tracking", metavar="FILE")
    args = argparser.parse_args()
    main(args)
