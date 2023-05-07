import sys
import io
logfile = io.StringIO()
sys.stdout = logfile
sys.stderr = logfile

import eel
import random
import sympy

num_digits = 20

lower_bound = 10**(num_digits-1)
upper_bound = 10**num_digits - 1

def search_prime():
    n = random.randint(lower_bound, upper_bound)
    p = sympy.nextprime(n)
    return p

p = 0
a = None

while len(str(p)) != num_digits and a == None:
    p = search_prime()
    a = sympy.primitive_root(p)

eel.init('web', allowed_extensions=['.js', '.html', '.css'])

@eel.expose
def greet(name):
    print(f"Hello, {name}!")

@eel.expose
def data():
    return p, a

@eel.expose
def calc(a_r, b_r):
    try :
        a_r = int(a_r)
        b_r = int(b_r)
        assert len(str(a_r)) >= 10 and a_r < p-1 and len(str(b_r)) >= 10 and b_r < p-1

        alice_public_key = pow(a, a_r, p)
        bob_public_key = pow(a, b_r, p)

        alice_shared_session_key = pow(bob_public_key, a_r, p)
        bob_shared_session_key = pow(alice_public_key, b_r, p)

        assert alice_shared_session_key == bob_shared_session_key

        return {
            'alice_public_key': alice_public_key,
            'bob_public_key': bob_public_key,
            'alice_shared_session_key' : alice_shared_session_key,
            'bob_shared_session_key' : bob_shared_session_key
        }
    except:
        return {
            'alice_public_key': "",
            'bob_public_key': "",
            'alice_shared_session_key' : "",
            'bob_shared_session_key' : ""
        }


eel.start('index.html', size=(900, 600))