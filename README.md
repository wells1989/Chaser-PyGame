# PyGame Chaser game

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Project Notes](#project-notes)

## Description
This PyGame based GUI project is a 2 player game, focusing on players obtaining the most points possible and attempting to trap / chase the other player to end the game. There are also several bonus cells that give the players extra turns / the ability to break through already visited cells to escape a trapped position.


**Tech-stack: python / PyGame**

**Project Areas: Dynamic GUIs with Pygame, advanced game / winning conditions / conditional PyGame rendering based off game conditions / managing multiple PyGame screen displays**

## Installation

1. Clone the repository:

   ```bash
   gh repo clone wells1989/Chaser-PyGame

2. Install dependencies:

   ```bash
   pip install -r requirements.txt 


## Usage
### Gameplay
- Players each start at a random position at the edge of the grid.
- Players move either horizontally or vertically, and can only move to new squares
- \* cells provide a random bonus payout / an extra turn for the current player / a break card for the current player (which allows them to go into previously visited squares / escape out of a trapped position)
- The game continues until one player is trapped in a position, at which point the player with the most points wins the game
- The players can view the rules / restarts the game at any point, and when the game is won the players can choose to play again.

### Game GUI
- **Welcome screen / rules**

![Screenshot (583)](https://github.com/wells1989/Full-stack-blog/assets/122035759/cfab8e9a-e71c-4f49-b875-b4df4037b55c)

- **Game start**

![Screenshot (586)](https://github.com/wells1989/Full-stack-blog/assets/122035759/08cdd178-7f0a-4386-b3d9-009c07c15230)

- **Game end**

![Screenshot (587)](https://github.com/wells1989/Full-stack-blog/assets/122035759/d76b8386-9ff9-4e26-9dff-8d2769798a6b)
  

### Project Notes:
- The goal of this project was to develop more complex GUIs with PyGame to allow a more interactive user experience in addition to core back-end functionality

#### Future-development:
- Future versions could have incorporated more players or allowed players to save their high scores of each game. However due to the GUI focused purpose of this project, user login / saving scores was not included yet
