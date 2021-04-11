# Connection-Verification

**Run/output**
```
D:\github\Connection-Verification> python .\run.py
Success:   ['www.google.com', 80]
Success:   ['www.google.com', 443]
Failed:    ['www.google.com', 8080]
Success:   ['www.yahoo.com', 80]
Success:   ['www.yahoo.com', 443]
Failed:    ['www.yahoo.com', 8080]
Success:   ['www.thenetwork.guru', 80]
Success:   ['www.thenetwork.guru', 443]
Failed:    ['www.thenetwork.guru', 8080]
```
**yml files**
```
port_groups.yml         # Lets you assign a group of ports to 1 name
connection_rules.yml    # These are the rules you want to check (ACL lines in network device speak)
port_map.yml            # Lets you refrence a port by name rather than number: (ssh = port 22)
```