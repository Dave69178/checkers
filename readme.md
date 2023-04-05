# Checkers Program

## Background
After my inital foray into creating a Chess program and AI (Take a look [here](https://github.com/Dave69178/chess-program)!) I burnt out and moved onto other projects. The scale of the project had been quite 
large compared to anything else I had worked on and so progress was somewhat messy and inefficient. Even so, I had learnt a lot and now had a new found appreciation
for software design and its challenges.

Moving forward to the current day, creating a checkers game and AI was given as a coursework assignment for one of my university modules, and so here we are. After an initial messy attempt, I spent proper time planning and refactoring - attempting to follow SOLID-like principles as much as possible. 
This resulted in a much nicer overall experience, with cleaner seperation and interfaces between components. Still a lot of room for improvement; a reemergence of lackluster design as deadline day closed in.

## Features
 - "Zero" player: Watch an AI vs AI game
 - One player: Play against an AI opponent of a selected difficulty
 - Two player: Enjoy a game against a fellow human
 - "Help" feature - get reccomendations of good moves from the AI
 - Regicide mode - capturing a King results in the capturing checker being crowned and the turn ending

![checkers_game](https://user-images.githubusercontent.com/59281365/230127469-f2b3e3ca-18cc-4c9b-a2b3-8a89985edd65.png)

## Installation
Easiest method is to use the conda environment.yml.
  In the checkers/ directory that contains main.py, enter the following command:
    "conda env create --file=environment.yml". (conda must already be installed and callable from the terminal)
  This will create a conda environment called "checkers_env".
  Run "conda activate checkers_env" to activate the environment.
  In the checkers/ directory, run "python3 main.py" and the program should start.

If not using conda, the dependencies are specified in the environment.yml file and can be installed with pip.
The only dependencies are:
 - python=3.10
 - numpy=1.23
 - pygame


Uninstallation:
To remove the conda environment: "conda remove -n checkers_env --all".

This was created on Linux and doesn't run as cleanly on Windows, but functionality should be fine.

Some other notes regarding performance are within the report.

## Notes

 - Efficiency and AI performance are rather weak, something that I plan to address in an upcoming project (web app of a similar style).
 - Focus within the limited time period was on creating a bug free game and AI opponent (i.e. no magical moves).
 - The AI uses a minimax search algorithm with alpha-beta pruning.
