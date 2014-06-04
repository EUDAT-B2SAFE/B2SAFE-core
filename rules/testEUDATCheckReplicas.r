check{
		# *ePIDcheck="true",*iCATuse="true"
        # createPID("None", *source, "None", *pidd, "True");
        # CheckReplicas(*source, *destination, bool(*ePIDcheck), bool(*iCATuse));
        EUDATCheckReplicas(*source, *destination);
}

INPUT *source="/vzRZGEUDAT/comm_data/comm_file16.txt",*destination="/vzRZGE/center1_data/comm_file16.txt"
OUTPUT ruleExecOut

