#ifndef EUDAT_H
#define	EUDAT_H

#include "apiHeaderAll.h"
#include "rods.h"
#include "objMetaOpr.h"
#include "dataObjRsync.h"
#include "reGlobalsExtern.h"
#include "rsGlobalExtern.h"
#include "rcGlobalExtern.h"

int 
msiWriteToLog(msParam_t *in_msg, ruleExecInfo_t *rei);

int 
msiGetZoneNameFromPath(msParam_t *inPath, msParam_t *outZoneName, ruleExecInfo_t *rei);

int
msiBytesBufToStr(msParam_t* in_buf_msp, msParam_t* out_str_msp, ruleExecInfo_t *rei);

#endif	/* EUDAT_H */

