# virtual-chat
Following are the brief points that we have implemented.
1. Client had two threads. A read and write thread that works in parallel.
2. You can receive message even when one client is writing a message.
3. The server when receives a message, it categorizes it as a “command” or a “normal message”. The “command” is a message followed by “/”
4. We have implemented four commands in the program: Block, Unblock, Sleep, Quit, Change Name
5. Client is implemented as a class on server side. It has a name, string and an array of blocked clients.
6. The above-mentioned array stores the blocked clients. All clients receive the message except the ones that client has blocked.
