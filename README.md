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
Once all the dependencies are installed (found in the *Pipfile* file) you can run `python main.py` and the program should start correctly.

### Windows
I tried to run the project on my Windows system, and I can assure you it doesn't work...
So, while the goal of the project is to make this run on both systems without problems, for now I must say that **the project is unstable for the Windows platform**. If you wish to help on this matter be my guest.

## Limitations

For now only the *Network match* is not avaiable, it still has to be programmed. I'm working on getting a good and stable *Local match* first and then I
suppose to move on onto the network stuff. This is still a work in progress after all, remeber that.

## TODO list
- [ ] Making the project stable for Windows
  - [X] Solving the reading of the directional arrows
  - [X] Insert unicode escaped sequences to be printed as characters (Maybe as a new constant)
  - [X] Change the value of a constant based on the platform the game runs on (Windows prompt doesn't support every sequence)
- [X] Adding the *Quit* feature, to quit the game quickly.
- [ ] Adding nations name translation support
- [ ] Add the *Network match* feature
- [ ] Adjust, refactor and optimize code (This is the very last thing to do)
