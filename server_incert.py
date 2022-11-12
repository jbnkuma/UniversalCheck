from universalcheck import novell_library

LAGS = ""
LAGE = ""
aux = []
aux2 = []
hostname = []
for datas in LAGE.split(" "):
    hostname.append(datas.split(",")[1])
    aux.append(datas.split(",")[0])

for i in aux:
    aux2.append(i.split(":"))
d = []
for l in aux2:
    for h in hostname:
        d.append((h, l[0], l[1]))
obj = novell_library.DataBase("/tmp/log", "universalcheck/servers.db")
TABLE = "Servers"
statements = '''(Hostname, Ip, Port)'''
provisory = '''(?,?,?)'''

for g in d:
    obj.insertion(TABLE, statements, provisory, g)
