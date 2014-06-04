#
# This function will check all errors between source-Collection and destination-Collection
# Data with error will be pushed into fail.log which are able to be transfered later.
# Parameter:
# 	*srcColl	[IN]	Path of transfered Collection
#	*destColl	[IN]	Path of replicated Collection
#
# Author: Long Phan, Jülich
#
EUDATIntegrityCheck(*srcColl,*destColl) {
        # Verify that input path is a collection
        EUDATVerifyCollection(*srcColl);
        EUDATVerifyCollection(*destColl);
        msiSplitPath(*srcColl,*sourceParent,*sourceChild);
        msiStrlen(*srcColl,*pathLength);

        *Work=``{
                msiGetObjectPath(*File,*source,*status);
                logInfo("*source");
                msiSubstr(*source,str(int("``++"*pathLength"++``")+1),"null",*subCollection);
                *destination = "``++"*destColl"++``"++ "/" ++ "*subCollection";
                logInfo("*destination");
                EUDATSearchPID(*source, *ppid);
                if (*ppid == "empty") {
                        logInfo("PPID is empty");
                        *status_transfer_success = bool("false");
                        *cause = "PPID is empty";
                        EUDATUpdateLogging(*status_transfer_success,*source,*destination, *cause);
                } else {
                        logInfo("PPID is created *ppid");
                }
                # FIXME: is it possible to get CPID at source-location ?
                EUDATSearchPID(*destination, *cpid);
                if (*cpid == "empty") {
                        logInfo("CPID is empty");
                        *status_transfer_success = bool("false");
                        *cause = "CPID is empty";
                        EUDATUpdateLogging(*status_transfer_success,*source,*destination, *cause);
                } else {
                        logInfo("CPID is created *cpid");
                }
                EUDATCheckError(*source,*destination);
            }``;
        msiCollectionSpider(*srcColl,*File,*Work,*Status);
}


#
# Verify the format of collection
# 
# Parameter:
# 	*srcColl	[IN]	Path of Collection
#
# Author: Long Phan, Jülich
#
EUDATVerifyCollection(*srcColl) {
    logInfo("Verify that source input path *srcColl is a collection")
    msiIsColl(*srcColl,*Result, *Status);
    if(*Result == 0) {
        logError("Input path *srcColl is not a collection");
        fail;
    }
}


#
# Transfer Collection using msiCollRsync (like irsync)
# 
# Parameter:
#	*srcColl	[IN]	Path of transfered Collection
#	*destColl	[IN]	Path of replicated Collection
#
# Author: Long Phan, Jülich
#
EUDATTransfer(*srcColl,*destColl,*targetResc) {
        EUDATVerifyCollection(*srcColl);
        EUDATVerifyCollection(*destColl);

        writeLine("serverLog","Begin to transfer data using msiCollRsync");
        msiSplitPath(*srcColl,*sourceParent,*sourceChild);
        *destination = "*destColl" ++ "/" ++ "*sourceChild";

        writeLine("serverLog","srcColl = *srcColl, destination = *destination");
        msiCollRsync(*srcColl,*destination,*targetResc,"IRODS_TO_IRODS",*Status);
}



#
# transfer Collection 
# Step 1: applying msiCollRsync to transfer Collection
# Step 2: create/ update PID 
#
# Author: Long Phan, Jülich
#
EUDATTransferColl(*srcColl,*destColl,*transfer,*targetResc){

        msiStrlen(*srcColl,*path_originallength);

        # ----------------- Apply transfer using msiCollRsync ------------    
        if (*transfer == bool("true")) {
                EUDATTransfer(*srcColl,*destColl,*targetResc);
                logInfo("Data Transfer completely. Done!");
        }
        logInfo("Begin to create CPID/ update PPID");

        # ----------------- Build condition for iCAT --------------- 
        *sPATH = *srcColl ++ "%";
        *Condition = "COLL_NAME like '*sPATH'";
        *ContInxOld = 1;
        msiSplitPath(*srcColl,*sourceParent,*sourceChild);
        logInfo("sourceParent = *sourceParent, sourceChild = *sourceChild");
        msiStrlen(*sourceParent,*pathLength);

        # ----------------------------------------------------------
        msiMakeGenQuery("COLL_NAME,DATA_NAME",*Condition, *GenQInp);
        msiExecGenQuery(*GenQInp, *GenQOut);
        msiGetContInxFromGenQueryOut(*GenQOut,*ContInxNew);
        while(*ContInxOld > 0) {
                foreach(*GenQOut) {
                        msiGetValByKey(*GenQOut, "DATA_NAME", *Name);
                        msiGetValByKey(*GenQOut, "COLL_NAME", *Collection);
                        # get length of *Collection
                        msiStrlen(*Collection,*lengthtemp);
                        # get SubCollection
                        msiSubstr(*Collection,"0","*path_originallength",*subcollname);
                        
                        # -------------------- Get SubCollection. --------------------  
                        *PATH = *Collection++"/"++*Name;
                        msiSubstr(*PATH,str(int(*pathLength)+1),"null",*SubCollection);

                        # -------------------- Transfer Data Obj ----------------------
                        *Source = "*sourceParent" ++ "/" ++ "*SubCollection";
                        *Destination = "*destColl"++ "/" ++ "*SubCollection";
                        logInfo("Source = *Source, Destination = *Destination");
                        EUDATTransferSingleFile(*Source,*Destination);
                }
                *ContInxOld = *ContInxNew;
                if (*ContInxOld > 0) {msiGetMoreRows(*GenQInp,*GenQOut,*ContInxNew);}
        }
}
