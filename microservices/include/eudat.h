#ifndef EUDAT_H
#define	EUDAT_H

#include "apiHeaderAll.h"
#include "rods.h"
#include "objMetaOpr.h"
#include "dataObjRsync.h"
#include "reGlobalsExtern.h"
#include "rsGlobalExtern.h"
#include "rcGlobalExtern.h"
#include <string.h>

int 
msiGetFieldFromRodsObjStat(msParam_t *in_rodsObjStat, msParam_t *in_Field, msParam_t *out, ruleExecInfo_t *rei);

int 
msiWriteToLog(msParam_t *in_level, msParam_t *in_msg, ruleExecInfo_t *rei);

int 
msiGetZoneNameFromPath(msParam_t *inPath, msParam_t *outZoneName, ruleExecInfo_t *rei);

int
msiBytesBufToStr(msParam_t* in_buf_msp, msParam_t* out_str_msp, ruleExecInfo_t *rei);

int
msiReplaceSlash(msParam_t *inPath, msParam_t *outPath, ruleExecInfo_t *rei);

#endif	/* EUDAT_H */

