check{
        createPID("None", *source, "None", *pidd, "True");
        CheckReplicas(*source, *destination, bool(*ePIDcheck), bool(*iCATuse));
}

INPUT *source="/vzRZGEUDAT/comm_data/comm_file16.txt",*destination="/vzRZGE/center1_data/comm_file16.txt",*ePIDcheck="true",*iCATuse="true"
OUTPUT *pidd,ruleExecOut

