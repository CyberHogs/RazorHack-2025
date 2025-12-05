# Intro Wi-Fi Challenges

## Description:
Three training challenges for my WIFI challenges with demo video.  The expectation was for competitors to have to look up how to do these challenges and how to use the Aircrack-ng suite.

**Training Demo Video:** https://www.youtube.com/watch?v=z3wAcBmOVkY

## Challenge 1: Systems Check

To start peering into the invisible wireless networks around you, your device must have a compatible Wi-Fi card connected.  Any device that can use Wi-Fi has a Wi-Fi card (with an antenna), whether connected internally or externally through USB.  In Linux, they show up as network *interfaces* with the name `wlan`.  Your VM has some interfaces connected already.  One way to see them is to use the `ip a` command.

How many wireless interfaces are connected to the machine?
<br>Flag: `flag{3}`

## Challenge 2: Mailbox Shenanigans

By default, Wi-Fi interfaces are configured to only listen to broadcast packets or packets that have the device’s MAC address attached.  It’s like the Wi-Fi card is shuffling through an apartment mailbox and looking for letters addressed to itself or to everyone.  It will disregard anything specifically addressed to a different person (or device).  However, we can tell the interface to read everything it can and ignore who it is addressed to, allowing you to conduct wireless network reconnaissance.  There is a suite of Linux tools designed around Wi-Fi hacking called *Aircrack-ng* that can be used to place interfaces into *monitor* mode, among many other uses.  The machine already has the tools installed, and they will be used for all the wireless challenges.

Place the `wlan0` interface into monitor mode.  What is its name after doing this?

Command needed: `airmon-ng start wlan0`
<br>Flag: `flag{wlan0mon}`

## Challenge 3: Yo, those are my packets, bro…

Finally, now that we have a Wi-Fi interface in monitor mode, we can start looking around and *capturing packets*.  Another command in the Aircrack-ng suite can do this.

How many wireless networks are there?

Command needed: `airodump-ng wlan0mon`
<br>Flag: `flag{8}`
<br>*There are 10 networks total, but the last two are not be visible using just the basic airodump command and are dealt with in later challenges.*
