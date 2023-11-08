import os
import subprocess
import datetime

def findEmailContacts(sessionid, email):
    fname = sessionid + str(datetime.datetime.now()).replace(":", "").replace("@", "") + ".txt"
    b = open(fname, "w")
    path = os.path.join(os.getcwd(), "holehe-master")
    print(path)
    a = subprocess.run(f"holehe {email}", stdout = b, cwd="C:\\Users\\parva\\Documents\\vervathon-2023\\holehe-master")
    b.close()
    c = open(fname, "r")
    webs = []
    for i in c.readlines():
        if "[!]" not in i and ("[+]" in i or "[-]" in i) :
            webs.append(i.strip())
    c.close()

    os.remove(fname)

    return webs