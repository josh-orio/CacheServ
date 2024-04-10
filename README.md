# CacheServ
A socket level server, with file caching, written in Python.

## The Goal

The intention was to build a simple socket communication system with caching, for accelerated transferring files.

When testing machine learning programs, they are prone to crashing. When you reload the program, you of course have to reload the dataset. With large datasets, it means you wait often >10 seconds before you even get going. 

This is long enough to lose focus and go back to thumbing through TikTok.

Having a seperate process which doesn't crash so much and keeps the most recently used files in RAM, you can avoid having to hit a much slower disk. This method does tradeoff maximum dataset capacity for start-up speed gains.

This was developed with a home network in mind, so the idea of hot storing a dataset on another local machine is not really feasible, because the network is too slow. The program was at one point tested to run on two machines but page sizes have to be small and data transfer takes too long.

## The Implementation

### tx_rx.py

The file tx_rx.py contains functions which do most of the work.

Initially these functions would just blindly chuck data at each other. Errors arose... 

Just sending a large file results in buffer overflow, so paging has to be implemented. Larger page sizes generally get the job done quicker, with one big caveat. When transmitting data between two local machines, a page size of >4096 bytes will never get through.

To remedy this, an md5 checksum is also sent along with each page. It allows the receiver to realise what its reading off the buffer is wrong. The rx() function signals for a resend when it realises it has received a corrupt page.

Asking for a retransmission causes errors, which is a result of two issues. (I think)

1. Sometimes between signalling a corrupt page and receiving the replacement page, random data (presumably what was supposed to arrive first time around) appears in the buffer, thrashing the page *again*.

2. The page size is still too large, and the transmitter won't send a smaller page, so it gets garbled again in transmission.

To clarify, this issue only arises when transmitting between two machines. Pages always arrive perfectly when transferring between two processes on one machine.

### server.py 

server.py provices the interface for CacheServ. It waits to accept a connection and when it receives one, tries to interpret a (JSON) command from a client.

Commands implemented are `ls` to list a directory and `read` to copy data.

`ls` will an (str) list of the files in the directory. server.py has a variable called 'serving_directory', this is the root of the server. The 'dir' argument of the `ls` command allows the client to list a sub-directory of the serving directory.

`read` takes a file name argument, and returns data in two ways, first looking through the cache and if the file is not found it will be read from the disk. Once data has been sent back to the client, the cache will be trimmed to make sure its size is within the limit set by the variable 'cms'.

If a `write` command was implemented it would be important to make sure that data in the cache is not older than data on the disk. This is simple, either purge a file with the same name from cache when writing to disk, or check when reading from cache that the file on disk is not newer.

## Possible Improvements

1. Before asking for retransmission of a corrupt page, wait for a few milliseconds and clear the recv buffer. Stack overflow has something about this, but I didn't try to implement it. (https://stackoverflow.com/questions/1097974/how-to-empty-a-socket-in-python)

2. To fix large pages not getting through, the transmitter could modulate to smaller page lengths e.g. 4096 bytes -> 1024 bytes.

3. To improve performance of server.py, a command could be added to pre-load a file into RAM. This doesn't seem to have many use cases though, because the client process could do its own pre-loading.

## The Future

This program won't be developed further, unless I want to fix the retransmission errors.  (I don't - 10.4.24)

I realise while debugging this program, C++ would have been cooler.
