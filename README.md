# Scrapper for allo.com search tips

Project include 3 logic parts:

 * db_manager - layer of working with db
 * tips_generator - generate all possible combination chars and digits, after that put into db
 * parser - fetch async requests, process response data, and save responses into db

## Requriments
* Python3.5+
* Ubuntu 18.04(tested a such system, but it must works independent on platform)

## Why asynchronus?
CPython (a typical, mainline Python implementation) still has the global interpreter lock so a multi-threaded application (a standard way to implement parallel processing nowadays) is suboptimal. That's why multiprocessing may be preferred over threading. But not every problem may be effectively split into almost independent pieces, so there may be a need in heavy interprocess communications. That's why multiprocessing may not be preferred over threading in general.

asyncio is a method to effectively handle a lot of I/O operations from many simultaneous sources w/o need of parallel code execution. So it's just a solution (a good one indeed!) for a particular task, not for parallel processing in general.

## Why aiohttp client?
Aiohttp recommends to use ClientSession as primary interface to make requests. ClientSession allows you to store cookies between requests and keeps objects that are common for all requests (event loop, connection and other things). Session needs to be closed after using it, and closing session is another asynchronous operation, this is why you need async with every time you deal with sessions.

## For what semaphore?
Sockets are just file descriptors, operating systems limit number of open sockets allowed. How many files are too many? I checked with python resource module and it seems like it’s around 1024. How can we bypass this? Primitive way is just increasing limit of open files. But this is probably not the good way to go. Much better way is just adding some synchronization in your client limiting number of concurrent requests it can process. I’m going to do this by adding asyncio.Semaphore() with max tasks of 1000.

## Running gide

```
# pip install -r requirements.txt
# python parser.py
```


#### Enjoy it and have a nice mood (^.^)