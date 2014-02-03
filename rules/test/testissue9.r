# add new user from other Zone for data object in order to execute remote-script

issue9 {
	EUDATsetAccessZone(*path,*name,*zone);
}

INPUT *path="/DATACENTER/PHANreplica/Coll17/csc10.ta", *name="rods", *zone ="DATACENTER2"
OUTPUT ruleExecOut