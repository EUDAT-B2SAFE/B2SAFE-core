test {
        #setCollectionForLogFiles(*logStatisticalFilePath,*logFailedFilesPath, *ReplFr, *ReplTo);

        #writeLine("serverLog","TEST CREATE LOGGING *test");
        #createLogging();
		
        #writeLine("serverLog","TEST UPDATE LOGGIN *update");
        #*b = bool("true");
        #*b = bool("false");
        #*path = "/COMMUNITY/DATA/file3.t";
        #updateLogging(*b,*path);
        #*Path = "/COMMUNITY/logfile/statistic.log";
        #*Str = "Number_of_failed_Files=0";
        #msiString2KeyValPair(*Str,*Keyval);
        #msiRemoveKeyValuePairsFromObj(*Keyval,*Path,"-d");
        #*Key3 = "Number_of_failed_Files";
        #*NewVal = 1;
        #*Val3 = "*NewVal";
        #createAVU(*Key3,"*Val3",*logStatisticalFilePath);

        writeLine("serverLog","TEST operations with LOG - exportLogFormatXML, backup, reset, remove");
        exportLogFormatXML();
        backupLogFiles();
        resetLogFiles();
        removeLogFiles();

}

INPUT *test = "Test create Logging files",*update = "Begin update Value for Key in AVU"
OUTPUT ruleExecOut
~                 