# coding=utf-8
"""
Game framework for Mirametrix eye tracker.

Author: Tomi Simsiö, Jiri Hamberg
"""

import argparse
import socket
import sys
from os import listdir
from os.path import isfile, join
import ConfigParser

import config
import xml_parser as parser
from modules.camera import Camera


profiledir = "game_profiles/"


def request_data(sock):
    sock.send(str.encode(
            '''<SET ID="ENABLE_SEND_POG_FIX" STATE="1" />\r\n
        <SET ID="ENABLE_SEND_EYE_LEFT" STATE="1" />\r\n
        <SET ID="ENABLE_SEND_EYE_RIGHT" STATE="1" />\r\n
        <SET ID="ENABLE_SEND_DATA" STATE="1" />\r\n'''
    ))


def get_xml_event_stream():
    """
    Get xml event stream from the eye tracking server or from a file.
    """
    if args.fake_eye_tracking:
        try:
            eye_tracking_stream = open(args.fake_eye_tracking)
        except IOError as e:
            print >> sys.stderr, "Could not open file: %s" % e.strerror
            exit(1)
    else:
        tcp_cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcp_cli_sock.connect((config.EYE_TRACKING_HOST, config.EYE_TRACKING_PORT))
            request_data(tcp_cli_sock)
        except socket.error as e:
            print >> sys.stderr, "Could not connect to eye tracking server: %s" % e.strerror
            sys.exit(1)
        eye_tracking_stream = tcp_cli_sock.makefile()
    return eye_tracking_stream


def list_games():
    files = [f for f in listdir(profiledir) if isfile(join(profiledir, f)) and f.endswith(".ini")]
    for f in files:
        print f[:-4]


def main():
    if not args.game:
        argparser.print_help()
        print
        print "Available games:"
        list_games()
        exit(0)
    inipath = profiledir + args.game + ".ini"
    if not isfile(inipath):
        print "File %s not found." % inipath
        exit(2)
    gameconfig = ConfigParser.ConfigParser()
    gameconfig.read(inipath)
    print "Starting with game profile '%s'... Press Ctrl+C to stop" % args.game

    camera = Camera(gameconfig)
    xml_event_stream = get_xml_event_stream()
    for event in parser.make_gaze_event_stream(xml_event_stream):
        camera.tick(event)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--fake-eye-tracking", metavar="FILE")
    argparser.add_argument("--game", "-g", help="Game to start")
    args = argparser.parse_args()
    main()
