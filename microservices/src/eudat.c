#include "../include/eudat.h"

int 
msiWriteToLog(msParam_t *in_msg, ruleExecInfo_t *rei) {
    char *msg;

    msg = parseMspForStr(in_msg);
    rodsLog(LOG_NOTICE, "msiWriteToLog :: %s", msg);

    return 0;
}

int 
msiGetZoneNameFromPath(msParam_t *inPath, msParam_t *outZoneName, ruleExecInfo_t *rei) {
    char *path;
    char tmp[MAX_NAME_LEN];
    char *ptr;  
    
    path = parseMspForStr(inPath);
    snprintf(tmp, MAX_NAME_LEN, "%s", path);
    strtok_r (tmp, "/", &ptr);
    fillStrInMsParam(outZoneName, tmp);
    
    return 0;
}

int
msiBytesBufToStr(msParam_t* in_buf_msp, msParam_t* out_str_msp, ruleExecInfo_t *rei) {
    rsComm_t *rsComm;
    char *inStr;
    bytesBuf_t *outBuf;

    int myInt;
    bytesBuf_t tmpBBuf, *myBBuf;

    rsComm = rei->rsComm;

    if (in_buf_msp != NULL) {
        myInt = parseMspForPosInt(in_buf_msp);
        if (myInt < 0) {
            if (myInt != SYS_NULL_INPUT) {
                rei->status = myInt;
                rodsLogAndErrorMsg(LOG_ERROR, &rsComm->rError, rei->status,
                        "msiDataObjWrite: parseMspForPosInt error for param2.");
                return (rei->status);
            }
        }
        myBBuf = in_buf_msp->inpOutBuf;
    }

    inStr = (char *) myBBuf->buf;

    fillStrInMsParam(out_str_msp, inStr);

    return 0;
}
