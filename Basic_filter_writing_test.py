import sys     #for reading standars input/output 
import subprocess   #used for gpg to encrypt messages 

def log(msg):
    print(f"filter-gpg: {msg}", file=sys.stderr)
    
    #this defines a simple login function 
    # adds filter-gpg to the message 
    # When stderr shows up it means the filter is working 
    
log("starting filter")    
    
# it calls the loggin function 
#    to make sure the filter is wroking properly 


for line in sys.stdin:  
	#this begans reading input lines from openSMTPD and 
    line = line.strip() 
    # removes any whitespaces or newline characters 
    
    if line == "":
        continue  
       #if line is blank, ignore and continue reading 
       
    if line.startswith("filter-transaction|"):
        print("proceed")
        #this line comes before the SMTPD filter
        # "I don't want to modify anything right now - procesed as usual 
    
    elif line.startswith("filter-dataline|"):
        print(line)
        #contains the actual body of the email 
        #we are priting them as they are now just to echo back 
        
    elif line.startswith("filter-end|"):
		    print("proceed")
        # Finalize message: run GPG encryption here
        #You could collect all the lines before this, encrypt 
        #     the full message using GPG, and then output the encrypted version here.

       # Right now it just says "proceed" — but this is where the 
       #     encryption logic will go.
       
    else:
        print("proceed")
