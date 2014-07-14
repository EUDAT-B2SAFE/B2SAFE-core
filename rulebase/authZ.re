#
# Rule: setup permission for other User from other Zone, defined as GROUP
# Arguments:
#   *path	[IN] the full iRODS path of the object
#   *otherUser	[IN] name of user who will be appended into GROUP
#   *otherZone  [IN] name of zone of *otherUser
# Author: Long Phan, JSC
#
EUDATsetAccessZone(*path,*otherUser,*otherZone) {
		
    msiSplitPath(*path,*collname,*dataname);
		
    *c = SELECT DATA_OWNER_NAME, DATA_OWNER_ZONE WHERE COLL_NAME = '*collname' AND DATA_NAME = '*dataname';
    foreach (*d in *c) {
        msiGetValByKey(*d,"DATA_OWNER_NAME",*owner);
        msiGetValByKey(*d,"DATA_OWNER_ZONE",*zone);         
    }
	 
    *dataOwner   = "*owner"++"#"++"*zone";
    *sessionUser = "$userNameClient"++"#"++"$rodsZoneClient";
	
    # Only Owner of Data have access right to add User into GROUP
    if (*dataOwner == *sessionUser) {
        writeLine("serverLog","Identity of User *sessionUser is confirmed");
        *addUser = "*otherUser"++"#"++"*otherZone";
        msiAddKeyVal(*Keyval,"GROUP", "*addUser");
        writeKeyValPairs('serverLog', *Keyval, " is : ");
        msiGetObjType(*path,*objType);
        msiAssociateKeyValuePairsToObj(*Keyval, *path, *objType);
        msiWriteRodsLog("EUDATsetAccessZone -> Added user= *addUser  to metadata GROUP of *path", *status);
    } else {
        writeLine("serverLog","Identity of User *sessionUser is not confirmed with Owner *dataOwner of *path");
    }
}

#
# Rule: filter ACL
# Arguments:
# 	*cmd  			[IN]	name of remote-script (ex. epicclient.py)
# 	*args			[IN]	argument of *cmd
#	*addr, *hint	[IN]	( see iexecmd -h)  
# 	*status			[OUT]	status of variable to decide whether script will be executed (true = yes, false = no)
# Author: Long Phan, JSC
#
EUDATsetFilterACL (*cmd, *args, *addr, *hint, *status) {
    *status = "false";
	
    if (*cmd == 'epicclient.py') {
        writeLine("serverLog","PYTHON Script *cmd is being accessed (remotely) with argument *args by user $userNameClient comes from $rodsZoneClient");
        writeLine("serverLog","--- begin to analyze argument *args");
        # Use (python script/ irods-microservice/ C-new-microservice) to filter the action ex. modify/delete and 
        # PID from argument *args
        # PID will be searched in iCAT to get dataOwner
        # After that it will be compared with $userNameClient and $rodsZoneClient. If match, action will be 
        # executed.
        # NOTICE: for first approach only actions modify and delete will be processed.

        *subargs = split(*args, " ");
        if (strlen(*args) > 0) {
            if (*args == "-h") {
                writeLine("serverLog","--- Argument -h");
                *status = "true";
            } else {
                *action = elem(*subargs,2);
                if (*action == "read" || *action == "search" || *action == "relation" || *action == "test") {
                    writeLine("serverLog","--- NOTICE action *action on PID");
		   			*status = "true";
                } else if (*action == "create") {

				# -------------------------------------- BEGIN TO FILTER ACTION CREATE ------------------------------------------
										
                    *param = elem(*subargs,3)

                    # *param should have format of URL 
                    # ----> ex. irods://egi-cloud17.zam.kfa-juelich.de:1247/COMMUNITY/DATA16/t13.test

                    writeLine("serverLog","WARNING action CREATE PID with URL *param");

				    # Filter logical address of data Object from *param

		  			getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
                    *templength = strlen(*serverID);
                    *tempID = substr(*param,0,*templength);
                    writeLine("serverLog","Length of *serverID = *templength with substr from *param = *tempID");
				    if (*tempID == *serverID) {
                        msiSubstr(*param,"*templength","null",*stringout);
						*pathDataObject = *stringout;
						writeLine("serverLog","Path of Data Object = *pathDataObject");
						
                        # figure out dataOwner of data Object and compare with user on session.
                        # If not dataOwner, fail 
                        
                        msiSplitPath(*pathDataObject,*collname,*dataname);
			
                        # ------------- Check the existence of Data Object in iCAT, 
						# ------------- if it exists in iCAT, continue check dataOwner. 
                        # If it's NOT exist in iCAT, continue deliver CREATE right. 
                        # ------------- Base on rule EUDATfileInPath of Giacomo -----------------
                        
                        *t = bool("false");	
						writeLine("serverLog","BEGIN TO CHECK WHETHER DATA EXIST");
			            *y = SELECT count(DATA_NAME) WHERE COLL_NAME = '*collname' AND DATA_NAME = '*dataname';
						foreach(*x in *y) {
						    msiGetValByKey(*x,"DATA_NAME",*num);
						    if(*num == '1') {				         	 				        *t = bool("true");
			                                writeLine("serverLog","Confirmed that DATA already existed under Coll_Name *collname with name *dataname");
			                            } 
						}
			
                        # -----------------------------------------------------------------------
										    
                        if (*t == bool("false")) {
                            writeLine("serverLog","Identity of user $userNameClient from $rodsZoneClient create PID without replication of data, script will be executed");

                            # SHOULD USER BE ALLOWED TO CREATE PID WITHOUT REPLICATION ? If yes, *status = true.
                            # Otherwise, set *status = false.

                            *status = "true";
                        } else {
                            writeLine("serverLog","EUDATfileInPath -> found file *dataname in collection *collname. Begin to check identity of user");

                        # ------------------------------------------------------------------------

                            *y = SELECT DATA_OWNER_NAME, DATA_OWNER_ZONE WHERE COLL_NAME = '*collname' AND DATA_NAME = '*dataname';
                            foreach (*x in *y) {
								msiGetValByKey(*x,"DATA_OWNER_NAME",*owner);
								msiGetValByKey(*x,"DATA_OWNER_ZONE",*zone);         
							    }
			  				if ($userNameClient == *owner && $rodsZoneClient == *zone) {			
                                writeLine("serverLog","User $userNameClient from *zone is confirmed as DataOwner of DataObject, action creating PID keeps going");	
                               
                                # Check whether this data Object already has one PID (in iCAT). If yes, fail. 
                                # ------------- Base on rule EUDATfileInPath of Giacomo -----------------
																							                              
                                *h = "META_DATA_ATTR_NAME = 'PID' AND COLL_NAME = '*collname' AND DATA_NAME = '*dataname'";
                                msiMakeGenQuery("count(META_DATA_ATTR_VALUE)",*h,*GenQInp);
                                msiExecGenQuery(*GenQInp, *GenQOut);
								*b = bool("false");
                                foreach(*GenQOut) {
                                    msiGetValByKey(*GenQOut,"META_DATA_ATTR_VALUE",*meta);
                                    if (*meta == '1') {
										#writeLine("serverLog","Name of file *dataname has AVU = *meta");
                                        *b = bool("true");		
                                    }														
                                }
                                if (*b == bool("false")) {
                                    writeLine("serverLog","Variable = *b, PID does not exist in AVU. Action CREATE PID will be executed");
                                    *status = "true";
                                } else {
                                    writeLine("serverLog","Variable = *b, PID already exist in AVU. Action CREATE PID will be canceled");
                                    *status = "false";
                                }																																			
                              
                                # -----------------------------------------------------------------------
                            
                            } else {
                                writeLine("serverLog","User $userNameClient from *zone is NOT confirmed as DataOwner of DataObject, action is being canceled");
                                *status = "false";   
                            }
                        }											
                    } else {
                        writeLine("serverLog","serverID is not correct, action CREATE will be canceled");
                        *status = "false";
                    } 										
                } else if (*action == "modify" || *action == "delete") {
                                
                # ------------------------ BEGIN TO FILTER ACTION MODIFY or DELETE -----------------------
                                		
                    writeLine("serverLog","--- WARNING action *action on PID");
                    *pid = elem(*subargs,3);
                    writeLine("serverLog","--- Begin to check identity of user");
                    writeLine("serverLog","--- Use PID *pid to search in iCAT to query dataOwner");

                    #*d = SELECT DATA_OWNER_NAME, DATA_OWNER_ZONE WHERE DATA_COMMENTS = '*pid';
		  			*d = SELECT DATA_OWNER_NAME, DATA_OWNER_ZONE, COLL_NAME, DATA_NAME WHERE META_DATA_ATTR_NAME = 'PID' AND META_DATA_ATTR_VALUE = '*pid';
                    foreach (*c in *d) {
                        msiGetValByKey(*c,"DATA_OWNER_NAME",*owner);
                        msiGetValByKey(*c,"DATA_OWNER_ZONE",*zone);
                        msiGetValByKey(*c,"DATA_NAME",*dataname);
                        msiGetValByKey(*c,"COLL_NAME",*collname);
                        writeLine("serverLog","Owner = *owner at Zone = *zone of DataObject *collname/*dataname is being accessed");
                    }
										
                    if ($userNameClient == *owner && $rodsZoneClient == *zone) {
				        *status = "true";
                        writeLine("serverLog","Identity of user $userNameClient from Zone $rodsZoneClient is confirmed as OWNER of DATA, script will be executed");
                    } else {
                        *user = "$userNameClient"++"#"++"$rodsZoneClient";
                        *e = SELECT META_DATA_ATTR_VALUE WHERE META_DATA_ATTR_NAME = 'GROUP' AND COLL_NAME = '*collname' AND DATA_NAME = '*dataname';
                        foreach (*f in *e) {
					    msiGetValByKey(*f,"META_DATA_ATTR_VALUE",*otherUser);
					    if (*otherUser == *user) {
                                *status = "true";
                                writeLine("serverLog","Access right of user $userNameClient from Zone $rodsZoneClient is confirmed in GROUP");
                                break;
                            }															
                        }
                        if (*status == "false") {
                            writeLine("serverLog","Access right is NOT confirmed, user *user is not a part of GROUP");
                        }
                    }								
                } else {                                		
                    writeLine("serverLog","Action is NOT confirmed ---");                                        
                }
            }   
        } else {
            writeLine("serverLog","Argument is unknown");
        }
   }

}
 
