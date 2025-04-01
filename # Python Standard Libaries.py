# Python Standard Libaries 
import os
import time     # Time Conversion Methods
import hashlib

# Python 3rd Party Libraries
from prettytable import PrettyTable     # pip install prettytable

# Psuedo Constants
targetFolder = input("Enter Target Folder: ")

#Local Functions
def HashFile(absPath): #returns sha-256 hash of file
    try:
        with open(absPath, 'rb') as target:
            
            fileContents = target.read()
            
            sha256Obj = hashlib.sha256()
            sha256Obj.update(fileContents)
            hexDigest = sha256Obj.hexdigest()
            return True, None, hexDigest
    except Exception as err:
        sys.exit("\nException: "+str(err))
 
def GetFileMetaData(absPath):
    ''' 
        obtain filesystem metadata
        from the specified file
        specifically, fileSize and MAC Times
        
        return True, None, fileSize and MacTimeList
    '''
    try:
        metaData         = os.stat(absPath)       # Use the stat method to obtain meta data
        fileSize         = metaData.st_size         # Extract fileSize and MAC Times
        timeLastModified = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(metaData.st_mtime))
        timeLastAccess   = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(metaData.st_atime))
        timeCreated      = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(metaData.st_ctime))
        
        macTimeList = [timeLastModified, timeLastAccess, timeCreated] # Group the MAC Times in a List
        return True, None, fileSize, macTimeList
    
    except Exception as err:
        return False, str(err), None, None 
        
# Start of the Script
print("Walking: ", targetFolder, "\n")

tbl = PrettyTable(['FilePath','FileSize', 'Last Modified', 'Last Accessed', 'Created on', 'SHA-256'])  

for currentRoot, dirList, fileList in os.walk(targetFolder):

    for nextFile in fileList:
        try:
            fullPath = os.path.join(currentRoot, nextFile)
            absPath  = os.path.abspath(fullPath)
            
            success, errInfo, fileSize, macTimeList = GetFileMetaData(absPath) #calls function to retrieve meta data about file
            success, errInfo, hexDigest = HashFile(absPath) #calls function to hash file          
        
            tbl.add_row( [ absPath, fileSize, macTimeList[0], macTimeList[1], macTimeList[2], hexDigest] ) 
        except Exception as err:
            print('Error:   ', str(err))   
                
tbl.align = "l" # align the columns left justified
# display the table
print (tbl.get_string(sortby="FileSize", reversesort=True))


print("\nScript-End\n")