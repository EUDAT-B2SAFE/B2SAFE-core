Installation/Upgrade
===================

The following describes the procedure to enable B2SAFE release-4.x.y

*NOTE*: This B2SAFE version makes use of the b2HANDLE library.
It can be found at: https://github.com/EUDAT-B2SAFE/B2HANDLE
Please use the included instructions in README.md to build and install B2HANDLE.
At the end of this installation the installation of B2HANDLE is described.

*NOTE*: iRODS is running as a normal user process. NOT as root. The package can
be build by any user. During installation of the package it will use: 
"/etc/irods/service_account.config" to set the ownership of the files.

*NOTE*: iRODS needs to be installed AND configured before installing/upgrading B2SAFE

Configure the yum repository for iRODS 4.1.12
---------------------------------------------
configure the repo as root:
```bash
cat > /etc/yum.repos.d/surfsara-irods.repo <<EOF
[surfsara-irods]
name=Surfsara iRODS repo
baseurl=https://software.irodspoc-sara.surf-hosted.nl/CentOS/7/irods-4.1.12
sslverify=0
gpgcheck=0
EOF
```


Configure the yum repository for iRODS 4.2.7
---------------------------------------------
configure the repo as root:

```bash
cat > /etc/yum.repos.d/surfsara-irods.repo <<EOF
[surfsara-irods]
name=Surfsara iRODS repo
baseurl=https://software.irodspoc-sara.surf-hosted.nl/CentOS/7/irods-4.2.7
sslverify=0
gpgcheck=0
EOF
```

Install pid-microservices for iRODS and B2SAFE
----------------------------------------------
```bash
sudo yum install msi-persistent-id b2handle irods-eudat-b2safe
```

After Installation / upgrade
----------------------------
After installation/upgrade actions. Always to do! Even after an upgrade.
The package b2safe has been installed in /opt/eudat/b2safe.
To install/configure it in iRODS do following as the user who runs iRODS:


### Install required python modules
As the user who runs iRODS do following:
```bash
cd /opt/eudat/b2safe/cmd
pip3 install --user -r requirements.txt
```

### convert install.conf to install.json if needed
When going from version 4.2.x or lower of B2SAFE to version 4.3 or higher convert the installation configuration.
As the user who runs iRODS do following:
```bash
cd /opt/eudat/b2safe/packaging
./convert_b2safe_conf_to_json.sh
```
Notice all the warnings and take them in to account.


### update install.json with correct parameters with your favorite editor.
As the user who runs iRODS do following:
```bash
sudo vi /opt/eudat/b2safe/packaging/install.json
```
| parameter                      | comment                                     |
|--------------------------------|---------------------------------------------|
| irods_default_resource         |                                             |
| server_id                      |                                             |
| server_api_reg                 | if no htp api make it same as server_id     |
| server_api_pub                 | if no htp api make it same as server_id     |
| handle_server_url              | needed for msi_pid uService                 |
| handle_private_key             | needed for msi_pid uService                 |
| handle_certificate_only        | needed for msi_pid uService                 |
| handle_prefix                  | needed for msi_pid uService                 |
| handle_owner                   | needed for msi_pid uService                 |
| handle_reverse_lookup_name     | needed for msi_pid uService                 |
| handle_reverse_lookup_password | needed for msi_pid uService                 |
| handle_https_verify            | needed for msi_pid uService                 |
| handle_users                   | needed for msi_pid uService. Users in iRODS |
| handle_groups                  | needed for msi_pid uService. Group in iRODS |
| authz_enabled                  | default=true                                |
| msg_queue_enabled              | default=false                               |


### install/configure it as the user who runs iRODS
```bash
source /etc/irods/service_account.config
sudo su - $IRODS_SERVICE_ACCOUNT_NAME -s "/bin/bash" -c "cd /opt/eudat/b2safe/packaging/ ; ./install.py"
```

DONE


## configure B2HANDLE
* Ask the handle hosting service which user to use for a certificate.
* Create a private/public keypair and create a derived certificate as described
in  http://eudat-b2safe.github.io/B2HANDLE/creatingclientcertificates.html.: 
```
  a> Generate public/private key pair
     i>  First download the software needed to create the private/public keypair.
         It can be found on: http://www.handle.net/download_hnr.html.
     ii> Execute ./hdl-keygen from hsj-8.1.1/bin directory 
  b> Send public key (.bin file) to your hosting service.
  c> Step 2: Upload of the user’s public key to the appropiate handle is executed by the hosting service
```
* Ask hosting service which username/password to use for reverselooup.
* Test using curl

