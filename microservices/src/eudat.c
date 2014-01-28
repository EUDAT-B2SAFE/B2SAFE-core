#include "../include/eudat.h"

int 
msiGetFieldFromRodsObjStat(msParam_t *in_rodsObjStat, msParam_t *in_Field, msParam_t *out, ruleExecInfo_t *rei) {
    rodsObjStat_t *rodsObjStatIn = NULL;
    char output[MAX_NAME_LEN];
    char *field;
    
    rei->status = 0;
    
    //process input parameter
    if(in_rodsObjStat->inOutStruct == NULL) {
        rei->status = -1;
        return rei->status;
    }
    rodsObjStatIn = (rodsObjStat_t *)in_rodsObjStat->inOutStruct;
    field = parseMspForStr(in_Field);
    if(field == NULL) {
        rodsLog(LOG_ERROR, (char *) "msiGetFieldFromRodsObjStat :: supplied field cannot be NULL.");
        rei->status = -1;
        return rei->status;
    }
    
    //extract requested field
    if(strcmp(field, "size") == 0 || strcmp(field, "SIZE") == 0) {
        snprintf(output, MAX_NAME_LEN, "%i", rodsObjStatIn->objSize);
    } else {
        rei->status = -1;
        rodsLog(LOG_ERROR, (char *) "msiGetFieldFromRodsObjStat :: unkown field supplied: [%s]", field);
    }
    
    //set output
    if(rei->status >= 0) {
        rei->status = fillStrInMsParam(out, output);        
    }
    return rei->status;
}

int 
msiWriteToLog(msParam_t *in_level, msParam_t *in_msg, ruleExecInfo_t *rei) {
    char *level;
    char *msg;
    
    level = parseMspForStr(in_level);
    msg = parseMspForStr(in_msg);
    
    if(strcmp(level, "debug") == 0) {
        rodsLog(LOG_DEBUG, "msiWriteToLog :: %s", msg);
    } else if(strcmp(level, "error") == 0) {
        rodsLog(LOG_ERROR, "msiWriteToLog :: %s", msg);
    } else {
        rodsLog(LOG_NOTICE, "msiWriteToLog :: %s", msg);
    }
    

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

/*
 * replace slash "/" symbol in string with an hyphen "_"
 * Input: String with / as absolute address of file ex. /tempZone/DATA/file.txt
 * Output: String with _ ex. _tempZone_DATA_file.txt
 * TODO: is there any better Search-Function after slash in C-library ?
 */
int msiReplaceSlash(msParam_t *inPath, msParam_t *outPath, ruleExecInfo_t *rei)
{
    rei->status = 0;
    char *strad =  parseMspForStr(inPath);
    int length = strlen(strad)+1;
    char *buffer = (char*) malloc(length);
    snprintf(buffer, length, "%s", strad);

    int i;
    for (i = 0; i < length; buffer[i] = buffer[i] == '/' ? '_' : buffer[i], i++)

    fillStrInMsParam (outPath, buffer);
    free(buffer);
    return rei->status;
}