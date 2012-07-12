#!/usr/bin/env python
import socket
import twitter
import sys
import StringIO

def twitter2irc(intext):
    if intext.startswith('/me '):
        return '\x01action' + intext[3:] + '\x01'
    return intext

def irc2twitter(intext):
    if intext.startswith('\x01action '):
        return '/me' + intext[7:-1]
    return intext

NEWLINE = '\r\n'

def init(host, port, consumer_key, consumer_secret, access_token_key,
        access_token_secret):
    api = twitter.Api(consumer_key, consumer_secret,
            access_token_key, access_token_secret)
    print api.VerifyCredentials()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    conn.settimeout(0.0)
    buff = ''
    nick = 'bot'
    last_mention = None
    while True:
        try:
            buff += conn.recv(1024)
        except socket.error:
            pass
        else:
            if NEWLINE in buff:
                index = buff.rindex(NEWLINE)
                buff, lines = buff[index + 1:], buff[:index]
                for line in lines.split(NEWLINE):
                    cmd, rest = line.split(' ', 1)
                    if cmd == 'NICK':
                        nick = rest
                    elif cmd == 'PRIVMSG':
                        name, rest = rest.split(':', 1)
                        api.PostUpdates('@%s %s' % (name.strip(), irc2twitter(rest)))
        for status in api.GetMentions(last_mention):
            conn.send(':%s PRIVMSG %s :%s%s' % (status.user.name, nick, twitter2irc(status.text[len(status.in_reply_to_screen_name)+3:]), NEWLINE))
            last_mention = status.id
    conn.close()


if __name__ == '__main__':
    if len(sys.argv) < 6 or sys.argv[1].count(':') != 1:
        print "Usage:", sys.argv[0], "localhost:6667 consumer_key",
        print "consumer_secret access_token_key access_token_secret"
        sys.exit(1)
    host, port = sys.argv[1].split(':')
    init(host, int(port), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
