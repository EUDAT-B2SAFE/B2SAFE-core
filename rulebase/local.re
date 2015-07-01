################################################################################
#                                                                              #
# EUDAT local specific functions                                               #
#                                                                              #
################################################################################

#
# Provides parameters for the connection with the EPIC service
# 
# Arguments:
# *credStoreType [OUT] [os | irods]: states if the file path is based on irods namespace 
#                      or on the filesystem
# *credStorePath [OUT] the path to the file containing the credentials to connect to an EPIC service
# *epicApi       [OUT] the reference URL for EPIC API
# *serverID      [OUT] the id related the irods service
# *epicDebug     [OUT] the debug level for the EPIC client scripts
#
# Author: Willem Elbers (MPI-PL)
#
getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug) {
    *credStoreType="os";
    *credStorePath="/srv/irods/current/modules/B2SAFE/cmd/credentials_test";
    *epicApi="http://hdl.handle.net/";
    *serverID="irods://<hostnameWithFullDomain>:1247"; 
    *epicDebug=2; 

    EUDATAuthZ("$userNameClient#$rodsZoneClient", "read", *credStorePath, *response);
}

# Provides parameters for the authorization mechanism
#
# Arguments:
# *authZMapPath  [OUT] the file path to the authorization map, 
#                      containing the authorization assertions.
#
# Author: Claudio Cacciari (Cineca)
#
getAuthZParameters(*authZMapPath) {
    *authZMapPath="/srv/irods/current/modules/B2SAFE/cmd/authz.map.json";
}

# Provides parameters for the logging mechanism
#
# Arguments:
# *logConfPath  [OUT] the file path to the logging configuration.
#
# Author: Claudio Cacciari (Cineca)
#
getLogParameters(*logConfPath) {
    *logConfPath="/srv/irods/current/modules/B2SAFE/cmd/log.manager.conf";
}

# Provides version of the B2SAFE
# 
# Arguments:
# *version  [OUT] the B2SAFE version.
# 
# Author: Claudio Cacciari (Cineca)
# 
getB2SAFEVersion(*version) {
    *version="3.0";
}

#
# This function is used to set up some parameters for the site in case you are
# going to use the EUDAT repository packages procedure to ingest data.
#
# Arguments:
# *protectArchive [OUT] Boolean, if 'true', the replicated file will become read only for the service user
# *archiveOwner [OUT] This is the iRods user owning the archive
#
# Author: S Coutin (CINES)
#
rp_getRpIngestParameters(*protectArchive, *archiveOwner) {
   *protectArchive = false;
   *archiveOwner = "rodsA";
}
