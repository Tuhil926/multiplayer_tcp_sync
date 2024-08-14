# Multiplayer tcp synchronisation

- This is like the basic template of the things required to synchronise the entire game state in a multiplayer setting.
- Basically, there is a state variable in the server, which is sent over in it's entirety to the clients.
- The clients can use this state to render the game.
- the clients send only their input to the server, and the server does the input handling to update the state accordingly.
- I haven't added any sort of predictive stuff in the client, so the input lag depends on the time taken for packets to make a round trip from the client to the server and back.
- I didn't make this object oriented or as a library, as I want every part of this system to be accessible so that it can be changed according to the needs of the game.
- I though of making a udp version of this as well, and I made a small prototype, but I don't think that's necessary, because I'm not really too fussed about speed in this case, I just need something that works reliably.

# How to run the demo:

- First start the server with `python3 server.py`
- You can start a client with `python3 client.py` and then enter the username of the player.
- You can start as many clients as you want, and for each one, you'll just need to enter an unique name.
- Each player is just a circle that can move around with wasd.
- if you want to connect across a local network, you'll need to change the address which the client connects to to the local address of the server

# How to customise:

- For the server, you'll need to put most, if not all your logic and code into the update_state_on_input and gameloop functions.
- For the client, it's a similar thing, where you add your game loop logic at the end of the file.
- you also might need to adjust the default values of state and inputs based on what your game needs.
- note that both input and state need to be arrays for this to work.

# New stuff I added:

1. Made the input from the clients be stored in a queue, so now every input is certain to be processed no matter what. The queue size is 1000, so there's very little chance that it'll overflow, especially considering the fact that the main loop runs 5 times as fast as the network loop. Also, for consistency, if the queue is empty after we process an input, I add the element back into the queue. This makes sense to do in my opinion, as we want the same input to persist when nothing is being received. Another reason is that if it wasn't there, then the movement won't be processed 4/5 times, making the movement stuttery.
