# -*- coding: utf-8 -*-
import sys
import time
import ftplib
from ftplib import FTP
import logging

# Use ftplib.FTP_TLS instead if you FTP host requires TLS.
# To retrieve it, you can use urllib.retrieve:
# import urllib 
# urllib.urlretrieve('ftp://server/path/to/file', 'file')

USER = 'test1'
PASS = '123!@#a'

########### MODIFY IF YOU WANT ############

SERVER = '192.168.180.169'
PORT = 1021
BINARY_STORE = False # if False then line store (not valid for binary files (videos, music, photos...))
ROOT_DIR = "weix\\"
###########################################

def connect_ftp():
    #Connect to the server
    ftp = FTP()
    ftp.connect(SERVER, PORT)
    logging.info("start login")
    login_res = ftp.login(USER, PASS)
    logging.info(login_res)

    dirlist = ftp.cwd(ROOT_DIR)
    ftp.dir()
    logging.info(dirlist)

    return ftp

def change_proper_dir(p_ftp_con, p_path):
    try:
        idx = p_path.index(ROOT_DIR)
        subdir = p_path[idx + len(ROOT_DIR) : p_path.rindex('\\')]
        logging.info('subdir: ' + subdir)
        p_ftp_con.cwd(subdir)
        # p_ftp_con.dir()

    except Exception as e:
        logging.error(e)

def is_binary(p_file_name):
    binary_type = ['dll', 'exe']
    for atype in binary_type:
        if p_file_name.endswith(atype):
            return True
    return False

def upload_file(ftp_connetion, upload_file_path):

    change_proper_dir(ftp_connetion, upload_file_path)
    #Open the file
    try:
        binary_flag = is_binary(upload_file_path)
        if binary_flag:
            ret_file = open(upload_file_path, 'rb')
        else:
            ret_file = open(upload_file_path, 'r')
        if ret_file:
            logging.info("open file ok")

        try:
        #get the name
            if upload_file_path.index('\\') >= 0:
                path_split = upload_file_path.split('\\')
            else:
                path_split = upload_file_path.split('/')

            final_file_name = path_split[len(path_split)-1]
        except:
            final_file_name = upload_file_path


        #transfer the file

        if is_binary(final_file_name):
            ftp_connetion.storbinary('STOR '+ final_file_name, ret_file)
        else:
            logging.info('Uploading file: ' + final_file_name)
            ret = ftp_connetion.storlines('STOR '+ final_file_name, ret_file)
            logging.info("upload result:" + ret)

        logging.info('Upload finished.')

    except IOError:
        logging.error ("No such file or directory... passing to next file")

if __name__ == '__main__':
    logging.basicConfig(filename='F:\\misc.py\\ftpup.log',level=logging.DEBUG)
    logging.info(sys.argv[1])

    upload_file(connect_ftp(), sys.argv[1])

    # leave some time for watching message prompted on console
    time.sleep(1)
