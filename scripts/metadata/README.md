B2SAFE Metadata Management
===========

This set of scripts aims to get metadata from the B2SAFE service and upload them to a GraphDB (Neo4J).

In order to get the list of options, just type:
```
$ ./b2safe_neo4j_client.py -h
usage: b2safe_neo4j_client.py [-h] [-dbg] [-d] confpath path

B2SAFE graphDB client

positional arguments:
  confpath       path to the configuration file
  path           irods path to the data

optional arguments:
  -h, --help     show this help message and exit
  -dbg, --debug  enable debug
  -d, --dryrun   run without performing any real change
```
For example, to execute it:
```
$ ./b2safe_neo4j_client.py conf/b2safe_neo4j.conf /cinecaDMPZone/home/rods/test1
```
Where the configuation file should look like this:
```
$ cat conf/b2safe_neo4j.conf 
# section containing the logging options
[Logging]
# possible values: INFO, DEBUG, ERROR, WARNING, CRITICAL
log_level=DEBUG
log_file=log/b2safe_neo4j.log

# section containing the sources for users and projects/groups'information
[GraphDB]
address=localhost:8888
username=
password=
path=/db/data/

[iRODS]
zone_name=cinecaDMPZone
zone_ep=dmp1.novalocal:1247
# list of resources separated by comma: res_name1:res_path1,res_name2:res_path2
resources=cinecaRes1:/mnt/data/irods/Vault
irods_home_dir=/cinecaDMPZone/home
irods_debug=True
```
The main assumption is that a file called *manifest.xml* is available under the irods path provided as input, which should be the root of the main collection described by the metadata.  
Therefore in this case we expect to find: /cinecaDMPZone/home/rods/test1/manifest.xml .  
The manifest file contains the structural metadata of the collection /cinecaDMPZone/home/rods/test1 and must be compliant to the METS format (http://www.loc.gov/standards/mets/).
Some examples are available in the test directory.
