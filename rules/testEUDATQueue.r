# 
# Test loop with EUDATQueue
#
test {		
	*Work=``{
		msiGetObjectPath(*File,*source,*status);
		logInfo("message = *source");
		EUDATQueue("push", *source, 0);   
        }``;
        msiCollectionSpider(*Collection,*File,*Work,*Status);	
}

INPUT *Collection = "/DATACENTER/DATA"
OUTPUT ruleExecOut
