#!/usr/bin/env python

import yaml, jinja2, os, crypt

def Download_ISO():
    os.system("sudo wget 'http://centos.hbcse.tifr.res.in/centos/7.6.1810/isos/x86_64/CentOS-7-x86_64-Minimal-1810.iso'")

def Create_mount_and_sync_folder():
    #removes previous mounted and synced folders
    os.system("sudo rm -rf iso_mount/ iso_rsync/")

    #creates mount and sync folder
    os.system("sudo mkdir ./iso_mount ./iso_rsync")

    #mount ISO to folder
    os.system("sudo mount -o loop CentOS-7-x86_64-Minimal-1810.iso ./iso_mount")

    #sync mount folder
    os.system("sudo rsync -av ./iso_mount ./iso_rsync")

    #unmount after sync
    os.system("sudo umount ./iso_mount")

def Encrypt_Password(passwd):
    return crypt.crypt(passwd, crypt.mksalt(crypt.METHOD_SHA512))

def CreateCentOS_KS():

    #Reading YAML file containig centos config info
    with open("centos_config.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    data_loaded['root_password'] = Encrypt_Password(data_loaded['root_password'])
    if data_loaded.get('users'):
        for user in data_loaded['users']:
            user['password'] = Encrypt_Password(user['password'])

    print("CentOS config info-->",data_loaded)
    #Loading and Rendering kickstart file using Jinj Template
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "Template_centOS_KS"
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(data_loaded)
    print("-"*10,"kickstart","-"*10)
    print(outputText)
    print("-"*10,"end","-"*10)

    #Writing kickstart to file
    f = open("./ks.cfg","w")
    f.write(outputText)

def Packaging_kickstart_file_into_ISO():
    cwd = os.getcwd() #get current working path
    os.system("sudo rm -rf CentOS-7-x86_64-Minimal-Custom.iso") #remove previous
    os.system("sudo cp ks.cfg ./iso_rsync/iso_mount/") #copy kickstart file to mount folder
    os.chdir("./iso_rsync/iso_mount/") #change directory

    #configuring isolinux.cfg
    os.system("sudo sed -i 's/append\ initrd\=initrd.img/append initrd=initrd.img\ ks\=cdrom:\/ks.cfg/' ./isolinux/isolinux.cfg")
    #Create ISO
    os.system("sudo genisoimage -o ../../CentOS-7-x86_64-Minimal-Custom.iso -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -J -R -v -T -V 'CentOS 7 x86_64' .")
    os.chdir(cwd)

    #implant checksum
    os.system("sudo implantisomd5 CentOS-7-x86_64-Minimal-Custom.iso")
    #removing sync and mount folder
    os.system("sudo rm -rf iso_mount/ iso_rsync/")

def Main():
    Download_ISO()
    Create_mount_and_sync_folder()
    CreateCentOS_KS()
    Packaging_kickstart_file_into_ISO()

if __name__=="__main__":
    Main()
