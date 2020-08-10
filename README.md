# TERMIKO!
![alt text](https://github.com/Jac-Lazza/termiko/blob/master/termiko_preview.png)

## The game
This is TERMIKO!, a terminal version of the RISIKO! game born as an idea while playing with friends.
The goal of the project is to create a game playable with friends remotely, both avaiable on Windows and \*nix
platforms and with a minimum level of entertainment.

### Game rules
The rules of this version of the game are slightly different from the ones found in the original one (both because
I'm too lazy to implement them or because they're not so easy to define in a program).
Both control commands and game rules can be found inside the game, in the main menu, I **highly suggest** you to read them
before start playing.

## Running the whole thing

### Linux
The project was made on a Linux system, so there should be no problems with this kind of platform (but I'm sure they will raise soon).
To run the game clone this repo and install the dependecies (I suggest to use a virtual environment, such as *pipenv*, but you can do as you want).
Once all the dependencies are installed (found in the file *Pipfile*) you can run `python main.py` and the program should start correctly.

### Windows
I tried to run the project on my Windows system, and I can assure you it doesn't work... From what I've seen it seems that the values for the
directional arrows are different from a Linux system and a Windows one, so this makes the menu useless. Also, if you get stuck in the menu on Windows,
by keeping pressed *CTRL+C* you get an exception that is not raised on Linux.
So, while the goal of the project is to make this run on both systems without problems, for now I must say that **the project is unstable for the Windows platform**. If you wish to help on this matter you're my guest.

## Limitations

For now only the *Network match* is not avaiable, it still has to be programmed. I'm working on getting a good and stable *Local match* first and then I
suppose to move on onto the network stuff. This is still a work in progress after all, remeber that.

## TODO-List
- Making the project stable for Windows
- Add the *Network match* feature
- Adjust, refactor and optimize code (This is the very last thing to do)
