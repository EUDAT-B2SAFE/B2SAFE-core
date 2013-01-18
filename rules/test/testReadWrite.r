test() {
   *path="/vzMPI/home/latuser/simple.txt";
   *input = "this;is;content1";
   writeFile(*path,*input);
   readFile(*path,*output);

   #msiWriteRodsLog(*out_STRING, *status);

   if(*input != *output) {
        msiExit("-1", "Read / Write test failed.");
   } 
   msiExit("0", "Read / Write test OK.");
}

INPUT null
OUTPUT *input,*output,ruleExecOut
