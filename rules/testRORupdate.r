#
# Test EUDATCreatePID and EUDATiRORupdate
#
iror{
		EUDATCreatePID("None", *source, "8/88888", bool("true"), *newPID)
        # EUDATcreatePID("None", *source, "8/88888", *pidd, "True");
        EUDATiRORupdate(*source,*newpid);
}
INPUT *source="/vzRZGEUDAT/comm_data/comm_file16.txt"
OUTPUT ruleExecOut
