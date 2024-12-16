

Distributed clipboard

This is the practical assigment for CT30A3401 Distributed Systems course. Written in python 3.5.2 

It is a simple python script that periodically checks if the contents of the hosts clipboard has changed and pushes said shange to the server (either local or remote host). It also checks the servers clipboard periodically and syncronizes it. The idea was to make a scrípt that would run in the background and allow for cut/copy on one machine and paste on the other without the need for any additional commands

Setup

    Set up the clippserver.py on a host (local or remote)

    Set the appropriate port and host in the config.py

    Install pyperclip pip package

Protocol

Communication is done over TCP socket using ASCII encoded messages. In the following format

REQUEST|PAYLOAD 

Requests from client to server are 'get', which gets the clipboard contents of the server and 'set' which sets new contents to the server.

From server to client the responces are 'ok' if the request succeeded and 'err' if it failed

Justification

Python was chosen as the programming language since the pyperclip module made manipulating the contents of the clipboard on multiple platforms simple, which allowed me to focus more on the communication.

As for why sockets were used for communication, it was partially because I had worked with web services in the last period and I wanted to try something "new" althoug sockets weren't exactly foreing to me either.

TCP was chosen because in the case of clipboard contents ensuring that it gets to its destination is more important than speed. UDP could also have been used but the risk of packet loss was the major problem with it. Also the data sent between the client and server is text data so the larger overhead wasn't a problem.

One problem I faced with this choise of architecture was the fact that I couldn't connect to another computer in my apartments network, which I assume is because of some router settings I cannot change so in perhaps a web service would have been a better choice in hindsight.
