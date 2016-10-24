################################################################################
#                                                                              #
# EUDAT local specific functions                                               #
#                                                                              #
################################################################################

# Provides the log level for the EUDAT specific rules
# 
# Arguments:
# *euLogLevel [OUT] the debug level for the EUDAT specific rules [0 | 1 | 2]
#                   0:ERROR, 1:INFO, 2:DEBUG
getEUDATLoggerLevel(*euLogLevel) {
    *euLogLevel=2
}


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

    getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
    if (*authzEnabled) {
        EUDATAuthZ("$userNameClient#$rodsZoneClient", "read", *credStorePath, *response);
    }
}

# -----------------------------------------------------------------------------
# Parse the credentials to connect to an EPIC server. A file called
# "credentials" MUST contain all the connection details in the home folder of
# the user running this rule.
# Parameters:
#   *baseuri            [OUT]   URI of the EPIC server
#   *username           [OUT]   username
#   *prefix             [OUT]   prefix
#   *password           [OUT]   password
#
# Author: Javier Quinteros, RZG
# -----------------------------------------------------------------------------
#
parseCredentials (*baseuri, *username, *prefix, *password) {

    *baseuri = 'https://epic3.storage.surfsara.nl/v2_test/handles/'
    *username = "<username>"
    *password = "<password>"
    *prefix = "<prefix>"
 
    getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled); 
    if (*authzEnabled) {
        EUDATAuthZ("$userNameClient#$rodsZoneClient", "read", "EPIC credentials", *response);
    }
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


#Provides parameters for the metadata management mechanism
#
# Arguments:
# *metaConfPath  [OUT] the file path to the metadata tool configuration.
# *enabled       [OUT] boolean value to enable (if true) globally the 
#                      json metadata writing
#
# Author: Claudio Cacciari (Cineca)

getMetaParameters(*metaConfPath, *enabled) {
    *metaConfPath="/srv/irods/current/modules/B2SAFE/cmd/metadataManager.conf"; 
    *enabled=bool("false");
}

#Provides parameters for the message management mechanism
#
# Arguments:
# *msgLogPath  [OUT] the file path to the message log file.
# *enabled     [OUT] boolean value to enable (if true) globally the
#                    the usage of the messaging system
#
# Author: Claudio Cacciari (Cineca)
#
getMessageParameters(*msgLogPath, *enabled) {
    *msgLogPath="/var/log/irods/messageManager.log";
    *enabled=bool("false");
}

#Provides parameters for some B2SAFE configurations.
# The plugin msifree_microservice_out is a bug fixing to avoid memory leak
# in case of collection replication involving thousands of files and the
# parameter msiFreeEnabled enables it.
# The CURL plugin 
#
# Arguments:
# *msiFreeEnabled  [OUT] if True the msiFree plugin must be deployed
# *msiCurlEnabled  [OUT] if True the msiCurl plugin must be deployed 
# *authzEnabled    [OUT] if True the authorization mechanism enforces the assertions 
#                        defined in the file retrieved by getAuthZParameters.
#
# Author: Claudio Cacciari (Cineca)
#
getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled) {
    *msiFreeEnabled=bool("true");
    *authzEnabled=bool("true");
    *msiCurlEnabled=bool("false");
}

# Provides version of the B2SAFE
# 
# Arguments:
# *version  [OUT] the B2SAFE version.
# 
# Author: Claudio Cacciari (Cineca)
# 
getB2SAFEVersion(*version) {
    *major_version = "3";
    *minor_version = "1";
    *sub_version = "2";
    *version = *major_version ++ "." ++ *minor_version ++ "-" ++ *sub_version;
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
