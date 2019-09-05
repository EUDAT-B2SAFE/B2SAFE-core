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
baseurl=http://software.irodspoc-sara.surf-hosted.nl/CentOS/7/stefan-wolfsheimer/devel/irods-4.1.12
sslverify=0
gpgcheck=0
EOF
```


Configure the yum repository for iRODS 4.2.6
---------------------------------------------
configure the repo as root:

```bash
sudo cat > /etc/yum.repos.d/surfsara-irods.repo <<EOF
[surfsara-irods]
name=Surfsara iRODS repo
baseurl=http://software.irodspoc-sara.surf-hosted.nl/CentOS/7/stefan-wolfsheimer/devel/irods-4.2.6
sslverify=0
gpgcheck=0
EOF
```

Install pid-microservices for iRODS and B2SAFE
----------------------------------------------
```bash
sudo yum install msi-persistent-id irods-eudat-b2safe
```

After Installation / upgrade
----------------------------
After installation/upgrade actions. Always to do! Even after an upgrade.
The package b2safe has been installed in /opt/eudat/b2safe.
To install/configure it in iRODS do following as the user who runs iRODS:


### Install required python modules
```bash
cd /opt/eudat/b2safe/cmd
sudo pip install -r requirements.txt
```

### update install.conf with correct parameters with your favorite editor.
```bash
sudo vi /opt/eudat/b2safe/packaging/install.json
```

|------------------------|------------------------|
| DEFAULT_RESOURCE       |                        |
| SERVER_ID              |                        |
| HANDLE_SERVER_URL      | needed for epicclient2 |
| PRIVATE_KEY            | needed for epicclient2 |
| CERTIFICATE_ONLY       | needed for epicclient2 |
| PREFIX                 | needed for epicclient2 |
| HANDLEOWNER            | needed for epicclient2 |
| REVERSELOOKUP_USERNAME | needed for epicclient2 |
| HTTPS_VERIFY           | needed for epicclient2 |
| AUTHZ_ENABLED          | default=true           |
| MSG_QUEUE_ENABLED      | default=false          |
|------------------------|------------------------|


### install/configure it as the user who runs iRODS
```bash
source /etc/irods/service_account.config
sudo su - $IRODS_SERVICE_ACCOUNT_NAME -s "/bin/bash" -c "cd /opt/eudat/b2safe/packaging/ ; ./install.py"
```

DONE


## installation of B2HANDLE
The customers need to install the b2handle library on the b2safe system and
create public/private keypairs and certificates and get the public key binary
uploaded before the upgrades.
This entails following:
* Download the b2handle code from: https://github.com/EUDAT-B2SAFE/B2HANDLE
* Create an rpm and install it on the b2safe system. With the necessary
dependencies. See the github page:

```bash
python setup.py bdist_rpm
````

```bash
yum install <created_rpm in dist directory> 
```

* Ask the handle hosting service which user to use for a certificate.
* Create a private/public keypair and create a derived certificate as described
in  http://eudat-b2safe.github.io/B2HANDLE/creatingclientcertificates.html.: 
```
  a> Generate public/private key pair
     i>  First download the software needed to create the private/public keypair.
         It can be found on: http://www.handle.net/download_hnr.html.
     ii> Execute ./hdl-keygen from hsj-8.1.1/bin directory 
  b> Send public key (.bin file) to your hosting service.
  c> Step 2: Upload the user’s public key to the....  is executed by the hosting service
```
* Ask hosting service which username/password to use for reverselooup.
* Test using curl
