# Mr. Robot CTF Writeup 

**Platform:** TryHackMe / VulnHub
**Difficulty:** Medium
**Category:** Web Exploitation / Privilege Escalation

---

## 🔒1. Reconnaissance

### Nmap Scan
I began by scanning the target machine to identify open ports and services.

```bash
nmap -sC -sV -p- <TARGET_IP>
```


**Results:**
* **Port 80/443:** Apache Web Server
* **Port 22:** Closed (SSH appears to be unresponsive)

![INSERT SCREENSHOT OF NMAP SCAN HERE](images/nmap_scan.png)

### Web Enumeration
I navigated to the website and found a terminal-style interface inspired by the show. 
I ran `gobuster` to find hidden directories, but checking standard files first yielded results.
![goubuster screenshot](Mr.Robot-THM/gobuster_scan.png)

**Checking robots.txt**
I navigated to `/robots.txt` and found two hidden files: `fsocity.dic` and the first key.

![INSERT SCREENSHOT OF ROBOTS.TXT HERE](path/to/screenshot2.png)

I downloaded the dictionary file `fsocity.dic` and confirmed the first flag.

> **Key 1:** `[REPLACE WITH FLAG 1 TEXT]`

### Viewing the fsociety.dic file

The `fsocity.dic` file contained many duplicate entries. So i used the sort & uniq command to filter unwanted entries

`sort fsocity.dic | uniq > sorted.dic`

Then it gave us a wordlist with lesser entries.

---

## 💥 2. Exploitation

### WordPress Login
I located a WordPress login page at `/wp-login.php`. Using the sorted dictionary file, I attempted to brute-force the credentials.

**Finding the Username:**
I verified that `elliot` was a valid user based on the error messages.

**Cracking the Password:**
I used Hydra to crack Elliot's password using the sorted wordlist.

`hydra -l elliot -P sorted.dic <TARGET_IP> http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In:F=Invalid username"`

![INSERT SCREENSHOT OF HYDRA SUCCESS HERE](path/to/screenshot3.png)

* **Username:** `elliot`
* **Password:** `ER28-0652`

### Getting a Reverse Shell
Once logged into the WordPress dashboard, I navigated to **Appearance > Editor**. I selected the **404 Template (404.php)**.

I replaced the PHP code with a standard PHP Reverse Shell (PentestMonkey), pointing the IP and Port to my attack machine.

![INSERT SCREENSHOT OF 404.PHP EDITOR HERE](path/to/screenshot4.png)

I started a Netcat listener:
`nc -lvnp 4444`

When I visited the 404 page URL, the shell connected.

![INSERT SCREENSHOT OF TERMINAL WITH SHELL HERE](path/to/screenshot5.png)

---

## 👤 3. Privilege Escalation (User)

### Finding Key 2
I browsed to `/home/robot`. I found the second flag file `key-2-of-3.txt`, but I did not have permission to read it. However, I found a raw MD5 password file.

`cat password.raw-md5`

* **Hash found:** `c3fcd3d76192e4007dfb496cca67e13b`

I used an online hash cracker to reverse the MD5 hash.
* **Cracked Password:** `abcdefghijklmnopqrstuvwxyz`

### Switching Users
Using the cracked password, I switched to the user `robot`.

`su robot`

I was then able to read the second key.

![INSERT SCREENSHOT OF READING KEY 2 HERE](path/to/screenshot6.png)

> **Key 2:** `[REPLACE WITH FLAG 2 TEXT]`

---

## 🚀 4. Privilege Escalation (Root)

### SUID Enumeration
I looked for files with the SUID bit set to see if I could escalate privileges to root.

`find / -perm -u=s -type f 2>/dev/null`

**Vulnerability Found:** `nmap`
I noticed `nmap` had the SUID bit set. This version of Nmap allows interactive mode, which can be used to escape to a shell.

### Rooting the Box
I ran Nmap in interactive mode and spawned a shell.

```bash
nmap --interactive
nmap> !sh
