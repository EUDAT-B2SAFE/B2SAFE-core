iRODS probe
===========

Nagios probe for the B2SAFE component iRODS

## Dependencies

It requires that the following iRODS packages are available in the environment:
http://irods.org/download/ -> iCommands CLI

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
Usage: check_irods.sh [-h|-v|-n|-d|-f file|-p file]
       -h help
       -v version
       -f the path of the iRODS environment json file. See iRODS documentation for details.
       -p the path of the file containing the password to connect to iRODS.
       -n implies no trash can enabled within the iRODS instance.
       -d debug enabled.
       -t timeout limit in seconds. The default is 30 s.
```
