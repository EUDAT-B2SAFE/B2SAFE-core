# Integrating B2SHARE and B2SAFE as a user
# 

import json
import requests
import os
import subprocess

API_TOKEN="Cti7PPvLhemuLDT20f6Jj0ragxcxp7N5rYAHHeC8PMYU8dWgtyc4MZEzAXgx"
API_URL = "https://trng-b2share.eudat.eu/api/"
COMMUNITY_ID = "0c97d6d2-88da-473a-8d30-2f4e730ed4a2" #EPOS
COMMUNITY_ID = "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095" #B2SHARE

# Download all data in a record from B2SHARE
#######################################################################
#NOTE: The B2SHARE API deals with lower case ids, but "home"/records/id
#lists id with capital letters.
r = requests.get('https://trng-b2share.eudat.eu/api/records/755f9026f1c241c9b3cb3e1abb322bce')

result = r.json()
title = result['metadata']['titles'][0]['title']

#download directory
folder = "B2SHARE_files"
os.mkdir(folder)

pid_dict = dict()
for entry in result['files']:
    pid_dict[entry['key'].replace(' ', '-')] = entry['ePIC_PID']

#download by PID NOTE: Does not work in test instance since no actionable PIDs
for entry in result['files']:
    content = requests.get(entry['ePIC_PID'])
    if content.status_code in range(200, 300):
        #save content as file
        with open(folder+"/"+entry['key'].replace(' ', '-'), 'wb') as out:
            out.write(content.content)

#download by B2SHARE path
resultfiles = requests.get(result['links']['files']).json()
for entry in resultfiles['contents']:
    content = requests.get(entry['links']['self'])
    if content.status_code in range(200, 300):
        with open(folder+"/"+entry['key'].replace(' ', '-'), 'wb') as out:
            out.write(content.content)
    
# Upload to iRODS/B2SAFE
#connect to iRODS
subprocess.call(['iinit'], shell=True)

#Create iRODS collection with "Title"
exit_code = subprocess.call(['imkdir '+ title.replace(' ', '-')], shell=True)

#iput -K 
for f in os.listdir(folder):
    exit_code = subprocess.call(['iput -K '+folder+'/'+f+" "+title.replace(' ', '-') ], shell=True)

#create some metadata in iRODS
# refer to PID for files
for f in os.listdir(folder):
    exit_code = subprocess.call(['imeta add -d '+title.replace(' ', '-')+'/'+f+" EUDAT/ROR "+pid_dict[f][22:] ], shell=True)
# TODO: When replicating, make sure to get ROR from iCAT and give to replication rule
#irule -F TrainingSetup/exampleRules/eudatReplication.r \
#   "*source='/aliceZone/home/rods/Published-Data'" \
#   "*destination='/aliceZone/home/rods/UploadColl'"

# Upload collection from B2SAFE to B2SHARE
###############################################################################
#Replication creates metadata in iCAT
#Transfer fields: PID, EUDAT/ROR and EUDAT/REPLICA to B2SHARE

#Data will stay in B2SAFE
#   -link via PID
#   -copy some B2SAFE metadata to B2SHARE metadata: EUDAT/ROR (mandatory), EUDAT/REPLICA
#       EUDAT/REPLICA: might change over time when more replicas are created --> update if mentioned in B2SHARE

create_draft_url = API_URL + "records/?access_token=" + API_TOKEN
data = '{"titles":[{"title":"Collection from B2SAFE"}], "community":"' + COMMUNITY_ID + '", "open_access":true, "community_specific": {}}'
headers = {"Content-Type":"application/json"}

draft = requests.post(url = create_draft_url,
                headers=headers,
                data = data )

assert draft.status_code in range(200, 300)

record_id = draft.json()['id']
print("Record created with id: " + record_id)

#2a. Get PIDs for files from iRODS
#These PIDs should be listed instead of creating new PIDs
irods_coll = '/aliceZone/home/rods/UploadColl'
p = subprocess.Popen(["ils "+irods_coll], shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()

irods_files = out.split('\n')[1:]
irods_files = [item.strip() for item in irods_files if item != '']

file_pid = {}
for f in irods_files:
    p = subprocess.Popen(["imeta ls -d "+irods_coll+'/'+f], shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    assert err == ''
    file_pid[f] = out.split('PID\nvalue: ')[1].split('\n')[0]    

#2b Real upload of data from B2SAFE to B2SHARE
#--> should not be neceassry
exit_code = subprocess.call(['iget -rK '+irods_coll], shell=True)
assert exit_code == 0

local_folder = os.getcwd()+"/"+os.path.basename(irods_coll)
files = os.listdir(local_folder)

for f in files:
    upload_files_url = draft['links']['files'] + "/" + f + "?access_token=" + API_TOKEN
    files = {'file' : open(local_folder+"/"+f, 'rb')}
    headers = {'Accept':'application/json','Content-Type':'application/octet-stream'}

    response = requests.put(url=upload_files_url,
        headers = headers,
        files = files )
    print response.status_code

#3. Get iRODS collection metadata and transfer to B2SHARE 
meta_dict = dict()
p = subprocess.Popen(["imeta ls -C "+irods_coll], shell=True, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
assert err == ''
avus = out

meta_dict['PID'] = avus.split('PID\nvalue: ')[1].split('\n')[0]
if 'EUDAT/ROR' in avus:
    meta_dict['EUDAT/ROR'] = avus.split('EUDAT/ROR\nvalue: ')[1].split('\n')[0]
if 'EUDAT/REPLICA' in avus:
    meta_dict['EUDAT/REPLICA'] = avus.split('EUDAT/REPLICA\nvalue: ')[1].split('\n')[0]

# 4. Patch the draft with extra metadata

#Collection metadata and file metadata as 'description'
patch_url = API_URL + "records/" + record_id + "/draft?access_token=" + API_TOKEN
patch = '[{"op":"add","path":"/descriptions","value":[{"description":"B2SAFE collection metadata: '+str(meta_dict)+'", "description_type":"SeriesInformation"},{"description":"B2SAFE file PIDs: '+str(file_pid)+'", "description_type":"TableOfContents"}]}]'
headers = {"Content-Type":"application/json-patch+json"}
response = requests.patch(url=patch_url, headers=headers, data=patch)

assert response.status_code == 200

# 5. Publish the record ! 
# Something is going wrong here when you use a community template but do not fill in any of the specific metadata, I get an 400 --> validation error.
# However, I can submit the draft via the web interface.
# The code below works fine for the general EUDAT metadata scheme.
patch = '[{"op":"add", "path":"/publication_state", "value":"submitted"}]'
response = requests.patch(url=patch_url, headers=headers, data=patch)
