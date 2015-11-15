"""
Parse xml stream on the fly. The xml stream should be provided as a
file-like object such as
    - a regular file
    - a file wrapper on a socket

Author: Jiri Hamberg (jiri.hamberg@cs.helsinki.fi)
"""

import xml.sax
import threading, json
from Queue import Queue
 
def _parse_fixation(xml_attrs):
    return {
        'id': int(xml_attrs['FPOGID']),
        'x': float(xml_attrs['FPOGX']),
        'y': float(xml_attrs['FPOGY']),
        'duration': float(xml_attrs['FPOGD']),
        'valid': bool(int(xml_attrs['FPOGV']))
    }
 
def _parse_left_eye(xml_attrs):
    return {
        'x': float(xml_attrs['LEYEX']),
        'y': float(xml_attrs['LEYEY']),
        'z': float(xml_attrs['LEYEZ']),
        'valid': bool(int(xml_attrs['LEYEV']))
    }  
     
def _parse_right_eye(xml_attrs):
    return {
        'x': float(xml_attrs['REYEX']),
        'y': float(xml_attrs['REYEY']),
        'z': float(xml_attrs['REYEZ']),
        'valid': bool(int(xml_attrs['REYEV']))
    }
 
def make_gaze_event_stream(file):
    """ 
    The file parameter should be a regular file (for testing purposes) or 
    a file wrapper around a socket created with socket.makefile().
    """
    def xml_reader():
        parser = xml.sax.make_parser(['xml.sax.IncrementalParser'])
        parser.setContentHandler(MirametrixRecEventHandler())
        parser.feed("<root>")
        data = file.read(1024)
        while(len(data) != 0):
            parser.feed(data)
            data = file.read(1024)
    reader_thread = threading.Thread(target = xml_reader)
    reader_thread.setDaemon(True)
    reader_thread.start()
    for event in iter(MirametrixRecEventHandler._queue.get, None):
        yield event
    parser.feed("</root>")
    parser.close()
     
class MirametrixRecEventHandler(xml.sax.ContentHandler):
    _queue = Queue()
    def startElement(self, tag, attrs):
        if tag == "REC":
            MirametrixRecEventHandler._queue.put(GazeEvent(attrs))

class GazeEvent(object):
    def __init__(self, attrs):
        self.fixation = _parse_fixation(attrs)
        self.l_eye = _parse_left_eye(attrs)
        self.r_eye = _parse_right_eye(attrs)

    def __str__(self):
        return "<GazeEvent fixation = {} l_eye = {} r_eye = {}".format(self.fixation, self.l_eye, self.r_eye)
    
    def json_encode(self):
        return json.dumps(self.__dict__)