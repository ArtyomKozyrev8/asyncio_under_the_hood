# asyncio_under_the_hood
Code snippets which demonstrate how asyncio works under the hood.

The project is based on video from PyCon 2015 and asyncio explanation by David Beazley:

https://www.youtube.com/watch?v=0oTh1CXRaQ0

The async_server.py looks quite similar to SelectSelector in
https://github.com/python/cpython/blob/3.9/Lib/selectors.py

How to run client in Terminal: 

`python client_side/socket_client.py 25`

`python client_side/client_for_async_server.py`

How to prove that async sever can work with several client simultaneously

1. Run script async_server.py

2. Run command `python client_side/client_for_async_server.py` in several terminals

3. See that terminal can receive messages in the same time, though Threads were not used in async_server.py