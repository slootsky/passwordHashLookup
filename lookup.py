import sys, locale
import msvcrt
from itertools import product
import hashlib
import sqlite3
import argparse

def mixString(istr):
    l = [(c, c.upper()) if not c.isdigit() else (c,) for c in istr.lower()]
    return ["".join(item) for item in product(*l)]

def getpwd():
	passwor = ''
	while True:
		x = msvcrt.getch()
		if x == '\r':
			return passwor
		sys.stdout.write('*')
		passwor +=x

def dbLookup(hash):
    global conn
    upperhash=hash.upper()
    cur=conn.cursor()
    cur.execute ('select count(*) from password_hash where hash=?', (upperhash,))
    count = cur.fetchone()
    if count[0] > 0:
        return "FOUND"
    else:
        return False
                  
    

parser=argparse.ArgumentParser()
parser.add_argument('-v','--verbose', action="store_true")
args=parser.parse_args()

conn = sqlite3.connect('sqlite/pwned-passwords.db')

# for testing
#pwd=u'pAssw0rd'
#pwd=u'password'

if args.verbose :
	pwd = raw_input("What is your best password?")
else:
	print "What is your best password?",
	pwd = getpwd()
	print ""

pwd=pwd.decode(sys.stdin.encoding or locale.getpreferredencoding(True))	

sha1 = hashlib.sha1()
sha1.update(pwd)

if args.verbose:
	print "{} : {} : {}".format(pwd,sha1.hexdigest(), dbLookup(sha1.hexdigest() ) )
else:
	if dbLookup(sha1.hexdigest() ):
		print "your password was FOUND"
	else:
		print "your password was not found"

findCount = 0		
permutationCount = 0
for p in mixString(pwd):
    permutationCount += 1
    if p <> pwd:
        sha1 = hashlib.sha1()
        sha1.update(p)
        if dbLookup(sha1.hexdigest()):
			findCount += 1
			if args.verbose :
				print "{} : {} : {}".format(p,sha1.hexdigest(), dbLookup(sha1.hexdigest() ) )
        
if findCount > 0 :
	print "there were {}/{} case insensitive matches of your password".format(findCount,permutationCount)
else:
	print "there were no case insensitive matches of your password"