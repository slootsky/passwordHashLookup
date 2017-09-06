import sys, locale
import msvcrt
from itertools import product
import hashlib
import sqlite3

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
                  
    

conn = sqlite3.connect('sqlite/pwned-passwords.db')

# for testing
#pwd=u'pAssw0rd'
#pwd=u'password'

#pwd = raw_itput("What is your best password?").decode(sys.stdin.encoding or locale.getpreferredencoding(True))

print "What is your best password?",
pwd = getpwd().decode(sys.stdin.encoding or locale.getpreferredencoding(True))

print pwd

sha1 = hashlib.sha1()
sha1.update(pwd)
print "{} : {} : {}".format(pwd,sha1.hexdigest(), dbLookup(sha1.hexdigest() ) )
for p in mixString(pwd):
    if p <> pwd:
        sha1 = hashlib.sha1()
        sha1.update(p)
        if dbLookup(sha1.hexdigest()):
            print "{} : {} : {}".format(p,sha1.hexdigest(), dbLookup(sha1.hexdigest() ) )
        