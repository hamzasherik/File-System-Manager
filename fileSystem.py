import math

class fileSystemManager:

    #constructor to instantiate num of blocks and storage capacity
    def __init__(self, storageCapacity: int, blockSize: int):
    
        #storageCapacity units: MB
        self.storageCapacity = storageCapacity
    
        #blockSize units: KB 
        self.blockSize = blockSize
        
    #determines number of blocks
    def numberOfBlocks(self):
    
        #blockSize represents the coefficient you multiply by 2^10 (for kilobytes in binary)
        blockSizeBinary = self.blockSize * (2**10)
        
        #storageCapacity represents the coefficient you multiply by 2^20 (for megabytes in binary)
        storageCapacityBinary = self.storageCapacity * (2**20)
        
        #divide storage capacity in binary by block size in binary to get number of blocks
        numBlocks = storageCapacityBinary / blockSizeBinary
        
        return int(numBlocks)
        
    #creates file system based on storageCapacity and blockSize using a 3D array where x-elements represent all blocks. The x-element can be either 0 or 1; 0 represents a free
    #block, and 1 represents an occupied block. The y-elements store the fileID. The z-element stores the blockID which is just the block's index in the array
    def createFileSystem(self, numberOfBlocks: int):
        
        #array to hold all blocks
        blocksArr = []
        
        #append numberOfBlocks number of blocks to the array and specify z-element to be the blockID
        for i in range(numberOfBlocks):
            blocksArr.append([0, 0, i])
        
        #store blocksArr as an object attribute so we can manipulate the same array after conducting any of the read, save or write functions
        self.blocksArr = blocksArr
        
        return

    #save function -> saves file to block(s) where size is in bytes
    def save(self, fileID: int, fileSize: int):
    
        #determine number of blocks this file will take
        numBlocksFile = math.ceil(fileSize / (self.blockSize * (2**10)))
        
        #used to determine if there are enough blocks left in storage to store the new file
        numBlocksFree = 0
        
        #empty array to store all free spaces in memory that the OS can save to (to be returned by the function)
        res = []
        
        #determine number of available blocks and store indeces of all free blocks that OS can save to
        for i in range(len(self.blocksArr)):
            if self.blocksArr[i][0] == 0:
                res.append(self.blocksArr[i][2])
                numBlocksFree += 1

        #if there are enough blocks available, then store this file in the first numBlocksFile available locations (fragmentation will occur here)
        if numBlocksFree >= numBlocksFile:
            
            #used to count number of blocks fileID is saved to
            ctr = 0    
                
            #iterate through blocksArr to find the first numBlocksFree elements where the storage space is not occupied and save the file to those elements
            for i in range(len(self.blocksArr)):
            
                #check if we've finished saving the entire file to storage
                if ctr == numBlocksFile:
                    break
                
                else:
                
                    if self.blocksArr[i][0] == 0:
                        
                        #store fileID in y-element
                        self.blocksArr[i][1] = fileID
                        
                        #set the block to occupied
                        self.blocksArr[i][0] = 1
                        
                        ctr += 1
            
            #return list of blocks that OS can use to save the file            
            return res
        
        #not enough space to store this file. Print and error and return all avaiable blocks in memory
        else:
            print('not enough space to store this file!')
            return res


    #read function -> opens file to be read
    def read(self, fileID: int):
    
        #used to store blocks where fileID is stored in
        res = []
    
        #iterate through storage and find all blocks where fileID is saved in and save
        for i in range(len(self.blocksArr)):
            if self.blocksArr[i][1] == fileID:
                res.append(self.blocksArr[i])
        
        #check if such a fileID exists in storage        
        if len(res) > 0:
    
            #return list of blocks file is saved in
            return res
        
        #if no file with this fileID exists in storage, return a failure message and return empty array   
        else:
            print('No such file!')
            return res

    #delete function -> marks blocks free after file deletion
    def delete(self, fileID):
    
        #iterate through storage to find all blocks where fileID is saved to and free those blocks
        for i in range(len(self.blocksArr)):
            if self.blocksArr[i][1] == fileID:
            
                #set block to free
                self.blocksArr[i][0] = 0
                
                #remove fileID
                self.blocksArr[i][1] = 0
     
        return
        
################################################################
#driver code
################################################################

#storageCapacity
X = 1

#blockSize
Y = 1

#create fileSystemManager object
obj = fileSystemManager(X, Y)

#determine number of blocks
numBlock = obj.numberOfBlocks()

#create the file system data structure
obj.createFileSystem(numBlock)

#saving files to storage and saving return value to variable
save1 = obj.save(12345, 1200)
save2 = obj.save(42842, 1600)
save3 = obj.save(80791, 5000)
save4 = obj.save(12834, 1000)

#reading files from storage
res1 = obj.read(12345)
res2 = obj.read(80791)

#deleting files from storage
obj.delete(12345)
obj.delete(12834)

#saving new files to storage (this will show that fragmentation occurs)
save5 = obj.save(11111, 1000)
save6 = obj.save(22222, 1200)




