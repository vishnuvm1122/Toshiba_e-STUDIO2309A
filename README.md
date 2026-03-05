TOSHIBA e-STUDIO2309A LINUX DRIVER

DESCRIPTION
This project provides a simple Linux installation package and setup script
for the Toshiba e-STUDIO2309A multifunction printer.

It helps Linux users install, configure, and use the printer easily
through the CUPS printing system. The script automatically adds the
printer using its network IP address.

------------------------------------------------------------

FEATURES

- Easy driver installation for Linux
- Automatic printer setup using CUPS
- Network printing support (IP address)
- Socket printing support (Port 9100)
- Works with most Debian-based Linux distributions
- Simple command-line installation
- Lightweight and fast setup

------------------------------------------------------------

SUPPORTED LINUX DISTRIBUTIONS

Ubuntu
Debian
Linux Mint
Kali Linux
Parrot OS
Other Debian-based Linux systems

------------------------------------------------------------

REQUIREMENTS

Before installing the printer driver, make sure the following
packages are installed:

- CUPS printing system
- Root or sudo privileges
- Network connection to the printer
- Printer IP address

Install required packages:

sudo apt update
sudo apt install cups cups-client cups-bsd printer-driver-gutenprint -y

Enable and start CUPS service:

sudo systemctl enable cups
sudo systemctl start cups

Check CUPS status:

systemctl status cups

------------------------------------------------------------

INSTALLATION

Download or clone the repository:

git clone https://github.com/vishnuvm1122/Toshiba_e-STUDIO2309A.git

Enter the project directory:

cd Toshiba_e-STUDIO2309A_Linux_Driver

Give execution permission to the installer:

chmod +x Toshiba_e-STUDIO2309A_Driver

Run the installer:

sudo ./Toshiba_e-STUDIO2309A_Driver

When prompted, enter your printer IP address.


------------------------------------------------------------


TEST PRINTING

Print a test page:

lp /usr/share/cups/data/testprint

Check printer status:

lpstat -t

List installed printers:

lpstat -p

------------------------------------------------------------

TROUBLESHOOTING

Restart CUPS service:

sudo systemctl restart cups

Check printer network connection:

ping IP

Check printer port:

nc -zv IP 9100

------------------------------------------------------------

PRINTER INFORMATION

Model: Toshiba e-STUDIO2309A
Type: Monochrome Multifunction Printer

Functions:
Print
Copy
Scan

Print Speed:
Up to 23 pages per minute

Connection:
Ethernet
USB
Network Printing

------------------------------------------------------------

LICENSE

This project is open-source and free for educational and personal use.
