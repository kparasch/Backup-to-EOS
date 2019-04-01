#!/usr/bin/python

import os
import time
import datetime
import threading
import subprocess

def timestamp_now():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d %H:%M:%S | ')

def status_loop():
    while 1:
        time.sleep(1)
        if status != 'Done':
            print(timestamp_now() + '(5-min STATUS UPDATE) ' +status)
            f.write(timestamp_now() + '(5-min STATUS UPDATE) ' +status + '\n')
        else:
            break
        time.sleep(300)

def print_and_write(f,status):
    print(timestamp_now()+status)
    f.write(timestamp_now()+status+'\n')

status = '                                                                                                     '
temporary_target_folder = '/media/Storage/tmp'
host = ' kparasch@lxplus.cern.ch:'
#source_dir = '/media/Storage/test_tar'
#destination_path = '/afs/cern.ch/user/k/kparasch/public/annalisa'
source_dir = '/media/Storage/lbitsiko/Simulation_Studies'
destination_path = '/eos/project/e/ecloud-simulations/lbitsiko'

#######ignore folders that were ok previously#####
#ignore_list=[1 for i in range(45)]
#ignore_list[7]=0
#ignore_list[9]=0
#ignore_list[11]=0
#ignore_list[14]=0
#ignore_list[15]=0
#ignore_list[23]=0
#ignore_list[27]=0
#ignore_list[30]=0
#ignore_list[32]=0
#ignore_list[37]=0
#ignore_list[43]=0
#ignore_list[44]=0
##################################################

current_dir = os.getcwd()
os.chdir(source_dir)

if source_dir[len(source_dir)-1] != '/':
    source_dir += '/'
if temporary_target_folder[len(temporary_target_folder)-1] != '/':
    temporary_target_folder += '/'
if destination_path[len(destination_path)-1] != '/':
    destination_path += '/'
if os.path.exists(temporary_target_folder+'checksums.md5'): 
    os.remove(temporary_target_folder + 'checksums.md5')

log_name = temporary_target_folder+'annalisa.log'
f = open(log_name,'w')
#threading.Thread(target=status_loop).start()

print_and_write(f,'Source directory is: ' + source_dir)
print_and_write(f,'Temporary target directory is: ' + temporary_target_folder)
print_and_write(f,'Destination is: ' + host.strip()+destination_path)

#i = -1
for folder in os.listdir(source_dir):
    ######ignore folders that were ok previously#####
    #i+=1
    #if ignore_list[i] : continue
    #################################################
    source_folder = source_dir+folder
    m_timestamp = os.path.getmtime(source_folder)
    human_timestamp = time.strftime('%Y%m%d', time.gmtime(m_timestamp))
    folder=folder.replace('(','\(')
    folder=folder.replace(')','\)')
    target_archive = temporary_target_folder + human_timestamp + '_' + folder.strip() + '.tar.gz'

    status = 'Source folder is: ' + source_folder 
    print_and_write(f,status)
    status = 'Target archive is:  ' + target_archive
    print_and_write(f,status)

    status = 'Archiving and compressing  ' + folder + ' ...'
    print_and_write(f,status)
    os.system('tar -czf ' + target_archive+' '+ folder.replace(' ','\ '))
    status = folder + ' archive complete.'
    print_and_write(f,status)

    status = 'Creating checksum for ' + target_archive + ' ...'
    print_and_write(f,status)
    os.system('md5sum '+target_archive+' >> '+temporary_target_folder+'checksums.md5')
    status = 'Checksum for ' + target_archive + ' complete.'
    print_and_write(f,status)

    status = 'Copying ' + target_archive + ' to destination ...'
    print_and_write(f,status)
    #os.system('scp '+target_archive+host+destination_path)
    os.system('until (scp '+target_archive+host+destination_path+'); do sleep 10; done')
    status = target_archive + ' copying complete.'
    print_and_write(f,status)

    status = 'Deleting ' + target_archive + '  ...'
    print_and_write(f,status)
    target_archive=target_archive.replace('\(','(')
    target_archive=target_archive.replace('\)',')')
    os.remove(target_archive)
    status = target_archive + ' deleted.'
    print_and_write(f,status)

    print_and_write(f,' ')
    print_and_write(f,' ')
    print_and_write(f,' ')


#replace paths in checksums
fcheck = open(temporary_target_folder + 'checksums.md5','r')
fcheck_lxplus = open(temporary_target_folder + 'lxplus_checksums.md5','w')
for line in fcheck:
    line=line.split('/')
    fcheck_lxplus.write(line[0]+destination_path+line[len(line)-1])
fcheck.close()
fcheck_lxplus.close()

status = 'Copying checksums to destination ...'
print_and_write(f,status)
#os.system('scp '+temporary_target_folder+'lxplus_checksums.md5'+host+destination_path)
os.system('until (scp '+temporary_target_folder+'lxplus_checksums.md5'+host+destination_path+'); do sleep 10; done')
status = 'Copying checksums complete.'

print_and_write(f,status)
status = 'Checking checksums to verify integrity on destination ...'
print_and_write(f,status)
cmd = ['ssh', host.strip(': '), 'md5sum', '-c', destination_path+'lxplus_checksums.md5']
p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
out,err = p.communicate()
ts = timestamp_now()
out = out.replace('\n','\n'+ts)
err = err.replace('\n','\n'+ts)
print_and_write(f,ts+'STDOUT:\n'+ts+out)
print_and_write(f,ts+'STDERR:\n'+ts+err)
status = 'Checking complete.'
print_and_write(f,status)
status = 'Please inspect final output.'
print_and_write(f,status)

status = 'Done'

os.remove(temporary_target_folder + 'checksums.md5')
os.remove(temporary_target_folder + 'lxplus_checksums.md5')
f.close()
#os.system('scp '+log_name+host+destination_path)
os.system('until (scp '+log_name+host+destination_path+'); do sleep 10; done')
os.remove(log_name)

os.chdir(current_dir)
