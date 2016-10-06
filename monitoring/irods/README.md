iRODS probe
===========

Nagios probe for the B2SAFE component iRODS.
It is implemented as a bash script.

## Dependencies

It requires that the following iRODS packages are available in the environment:  
http://irods.org/download/ -> iCommands CLI  
It is also possible to add to your environment a repository containing the iRODS iCommands so that the dependency is solved automatically:  
http://rpm-repo.argo.grnet.gr/ARGO/[devel|prod]/[centos6|centos7]/

## Deployment

It is possible to just copy the script and the related configuration files to the wanted directory.  
Or to create a rpm package, following the next steps.  
Go to the directory monitoring/packaging.  
Execute the script create_rpm_package.sh.  
Deploy the rpm package.  
By default the script is place in:  
/usr/libexec/argo-monitoring/probes/b2safe/check_irods.sh  
The configuration files in:  
/etc/nagios/plugins/b2safe/irods

## Configuration

The script "check_irods.sh" relies on the authentication methods supported by iRODS.
Then it requires the setting of the irods user environment, creating a file like this:
```
{
    "irods_default_hash_scheme": "MD5", 
    "irods_default_resource": "cinecaRes1",
    "irods_home": "/cinecaDMPZone2/home/claudio", 
    "irods_host": "my.host.name", 
    "irods_match_hash_policy": "strict", 
    "irods_port": 1247, 
    "irods_user_name": "claudio", 
    "irods_zone_name": "cinecaDMPZone2",
    "irods_authentication_scheme": "native"
}
```
The values have to be replaced according to the local configuration.
Finally a second file is required, containing just the password for the iRODS user dedicated to the monitoring.
The script can be executed with the following input parameters:
```
Usage: check_irods.sh [-h|-v|-n|-d|-t time|-f file|-p file]
       -h help
       -v version
       -f the path of the iRODS environment json file. See iRODS documentation for details.
       -p the path of the file containing the password to connect to iRODS.
       -n implies no trash can enabled within the iRODS instance.
       -d debug enabled.
       -t timeout limit in seconds. The default is 30 s.
```
It uploads, reads, downloads and removes a file of few KB in size.  
It relies on plain iRODS icommand operations, without involving specific EUDAT rules.
It is up to the iRODS administrator, who sets the user dedicated to the monitoring, to decide how much "power" to give to that user. For example the execution of rules can be denied. The user can have a dedicated home space or share that of an existing project/community.
