# Battleship
A digital remake of the game Battleship with an intelligent AI agent.

## About
This is a version of the board game Battleship that has a human player against an AI. 

It features 2 random baseline methods as well as Q-Learning and Monte Carlo methods in order to create an AI that efficiently beats the human more times than not. 

Unfortunately the Monte Carlo aspect of the AI has not been implemented fully, but hopes to be so in the future. 

This project was implemented in Python and the entire user interface was successfully created by using pygame. 

## Requirements
python~=3.6

pygame~=1.9.6

numpy~=1.18.1

## Usage
To run:	`python3 main.py`

When the game start, drag all the ships (yellow rectangles) to the board. Double click to rotate.

If ready, press 'start'. Take turns hitting ships until all 5 ships are sunk.

Guide: Orange = Hit, Red = Sink, Green = Miss

## Note
** Currently the main.py file is set up to run the Q-Learning AI. The code for the random AI is commented out right below it.

## Visualization

![Battleship Board](https://github.com/kchonka/battleship/blob/master/visualization.png)
 
