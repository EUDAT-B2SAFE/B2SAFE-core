# 
# Test loop with EUDATSearchPID
#
test {		
	*Work=``{
		msiGetObjectPath(*File,*source,*status);
		logInfo("File = *source");
		EUDATSearchPID(*source, *existing_pid);        
        }``;
        msiCollectionSpider(*Collection,*File,*Work,*Status);	
}

INPUT *Collection = "/DATACENTER/DATA"
OUTPUT ruleExecOut
