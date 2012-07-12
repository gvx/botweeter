#!/usr/bin/env python
import socket
import twitter
import sys

def twitter2irc(intext):
	if intext.startswith('/me '):
		return '\x01action' + intext[3:] + '\x01'
	return intext

def irc2twitter(intext):
	if intext.startswith('\x01action '):
		return '/me' + intext[7:-1]
	return intext

def init(host, port, consumer_key, consumer_secret, access_token_key,
        access_token_secret):
    api = twitter.Api(consumer_key, consumer_secret,
            access_token_key, access_token_secret)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    conn.settimeout(0.0)
    while True:
        try:
            data = conn.recv(1024)
        except socket.timeout:
            pass
        else:
            #use twitter API
            #send data back to bot
            pass
    conn.close()


if __name__ == '__main__':
    if len(sys.argv) < 6 or sys.argv[1].count(':') != 1:
        print "Usage:", sys.argv[0], "localhost:6667 consumer_key",
        print "consumer_secret access_token_key access_token_secret"
        sys.exit(1)
    host, port = sys.argv[1].split(':')
    init(host, int(port), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
