# CentOS Custom ISO

Configuring Kickstart file:
-------

- Add or edit YAML file to configure kickstart file.

- Configurable Attributes
1. keyboard
2. language
3. root_password
4. timezone
5. users
6. size
7. packages

How To Run:
------
>python3 Generate_Custom_ISO.py
- Downloads iso
- Creates copy of ISO and adds kickstart file
- Add path to isolinux.cfg
- pask new ISO with checksum

>Dependencies:
- python3
- rsync
- mount
- genisoimage
- isomd5sum
- crypt
- jinja2
- yaml
- sed
