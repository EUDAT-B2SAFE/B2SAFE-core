B2SAFE
===========

B2SAFE service code for EUDAT project.

It is released under BSD license.

The EUDAT (http://www.eudat.eu) B2SAFE Service offers functionality to replicate datasets across different data centres in a safe and efficient way while maintaining all information required to easily find and query information about the replica locations. The information about the replica locations and other important information is stored in PID (Persistent IDentifier) records, each managed in separate administrative domains. The B2SAFE Service is implemented as an iRODS (http://www.irods.org) module providing a set of iRODS rules or policies to interface with the EPIC (http://www.pidconsortium.eu) handle API and uses the iRODS middleware to replicate datasets from a source data (or community) centre to a destination data centre.

---------------
Deployment
---------------

See install.txt .

---------------
Documentation
---------------

http://eudat.eu/services/userdoc

---------------
Known issues
---------------

- the iRODS server forks an irods agent for each client request: each irods agent handling a PID creation request allocates about 1 GB of memory/10^4 object registered, due to a memory leak.
Therefore in order to manage concurrent requests coming from, for example, 30 users, involving the registration of collections of 10^4 objects, the B2SAFE administrator should plan to provide at least 32 GB of memory dedicated to the B2SAFE instance (https://github.com/irods/irods/issues/2929).

- a similar issue is already tracked in the iRODS github:
https://github.com/irods/irods/issues/2928
But it is related to the iput operation with the bulk option.
And the leak is smaller: 2 GB of memory/10^6 object uploaded.
Therefore for 30 users running bulk upload in parallel of collection of 10^4 objects, just 600 MB are enough.
