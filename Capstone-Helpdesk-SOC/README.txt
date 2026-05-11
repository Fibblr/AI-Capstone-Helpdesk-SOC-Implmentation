AI-Enhanced SOC & Helpdesk Decision-Support System
Group: Cameron Edenburn & Jacob Moore

This project aims to sort SOC alerts and IT Tickets by priority and return a confidence score using the Cohere AI API.
--- FOLDER STRUCTURE ---
/soc_logic   - Contains the AI API client, data normalization, and severity scoring modules.
/templates   - Contains the HTML views for the Staff and Employee dashboards.
/static      - Contains the CSS styling.
app.py       - The core Flask application, routing, and SQLite database initialization.

SETUP:
DOWNLOAD TEST VM LINK GOOGLEDRIVE -------> https://drive.google.com/file/d/1vE7FTi5vk4poR6kDU2EKhS_kWOsJjVrV/view?usp=drive_link *WINDOWS 11*
                                  -------> https://drive.google.com/file/d/16nv--EiSX4_HCefz03qgZtdbNMoH9FI5/view?usp=sharing *LINUX*
***If the VM's are too much space you do not have to install windows 11 VM, just the Linux ones. The network adapter should be simillar if not the same! Just make sure your host
computer and Linux machines can communicate to each other*******


Credentials:
-----------------------
Windows 11 VM
    Username:CIOS 
    Password:P@ssw0rd
------------------------
Ubuntu Server (WAZUH) VM
    Username:test 
    Password:test
------------------------
Ubuntu Server (Flask) VM
    Username: flask
    Password: flask!
------------------------

***Make sure each VM has two network adapters, In VMWare click the VM tab then click the "edit virtual machine settings" to verify. If any adapter is missing you can add
or remove adapters in the options. Just make sure NAT IS FIRST!!!!!!!!*******
-Make sure network adapters are set as NAT, then the secondary is vmnet1(hostonly). 
-**I had hostonly but that may not be neccssary, NAT is 100 percent needed though!!****
    -Ubuntu IP: 192.168.1.50
    -Flask IP: 192.168.1.51
    -Windows IP: 192.168.1.49
    -Default Gateway/DNS/Subnet Mask: 192.168.1.1, 1.1.1.1, 255.255.255.0
    -Make sure all firewalls allow port 8081. (This is why we turned off ufw, so there would be no conflict)

Install VMWare Workstation ------>https://www.vmware.com/products/desktop-hypervisor/workstation-and-fusion

Configure Each Machine:
------------------------
Ubuntu 64 bit ------------> This is the Flask (App.py) server!

1. "sudo ufw disable"
2. "cd /home/flask"
3. Remove current project folder sudo rm -r AI-Capstone-Helpdesk-SOC-Implmentation
Get current project: "sudo git clone https://github.com/Fibblr/AI-Capstone-Helpdesk-SOC-Implmentation/tree/main/Capstone-Helpdesk-SOC"
4. "cd AI-Capstone-Helpdesk-SOC-Implmentation
5. "cd Capstone-Helpdesk-SOC"
6. "sudo nano .env"
    You can use your own Cohere API Key or Mine.
    IN .env TYPE THE FOLLOWING: COHERE_API_KEY=H+U2YA9v5iG0fP81?u5e??9*8egCBCfe
7. Press Ctrl + x then type "y" then enter to save the .env file.
8. "sudo python3 app.py"

    You should see the output:
    "SOC LOGIC Loaded Successfully"
    "*Serving Flask App 'App'"

***RECORD WHAT PORT AND IP THE APPLICATION IS RUNNING ON!!!
Leave the program running on the terminal in the background and nove on to the next VM.....
-----------------------------------------------------------------------------------------------------------------------------------------------
WAZUH (Ubuntu server for the Wazuh SIEM!!)

1. "sudo ufw disable"
2. "cd /home/flask"
3. Remove current project folder sudo rm -r AI-Capstone-Helpdesk-SOC-Implmentation
Get current project: "sudo git clone https://github.com/Fibblr/AI-Capstone-Helpdesk-SOC-Implmentation/tree/main/Capstone-Helpdesk-SOC"
4. "cd AI-Capstone-Helpdesk-SOC-Implmentation
5. "cd Capstone-Helpdesk-SOC"
6. "sudo nano .env"
    You can use your own Cohere API Key or Mine.
    IN .env TYPE THE FOLLOWING: COHERE_API_KEY=H+U2YA9v5iG0fP81?u5e??9*8egCBCfe
7. Press Ctrl + x then type "y" then enter to save the .env file.
8. "sudo python3 main.py"

    The output should look like
    "Listening to Authentication Alerts......"

Leave the app.py and main.py running on the terminal in the two different VM's in the background and move on to the next VM.....
---------------------------------------------------------------------------------------------------------------------------------------------------
***Ignore if you are using host system to view dashboard***

Windows 11 VM (The main VM to view the Flask App GUI) 
1.Under the network settings, click advanced then under tcp ipv4 double click the network adapter for the hostvm, the second adapter, to make
sure all network information is correct.
2. On Windows 11 VM go to a web browser and type http://Put the IP you recorded from the Flask server:8081
3. Logon using
    Test Credentials:
    - Staff Login: jacob / pass123
    - Employee Login: john / user123
4. Click on alerts to view contents
----------------------------------------------------------------------------------------------------------------------------------------------------
If you have any issues:
-Check IP Configuration/Adapter settings on all apps.
-Make sure .env is not empty
-Make sure all programs are still running
-Run the Flask server first



