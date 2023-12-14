# DATA_440_Final_Project_Football_Sim

My final project idea is to use the data from my independent study to create a football game simulator that allows a user to take on the role of an offensive coordinator and decide whether to run or pass the ball on a given play, and a model will return the outcome of that play, whether that be a number of yards gained, a touchdown, a turnover, etc. This outcome will then be used to update the game situation and the user is given the chance to choose once more. The simulation will operate on a play-clock, and it will result in either a win or a loss.

## Data:
- Pro Football Focus (PFF)
- NFL play-by-play data from 2013-2022

## Streamlit Link:
To play the game and test out the simulation yourself, visit the following link:
https://gridiron-guru-football-sim.streamlit.app

## Important Info
- All randomly simulated instances in the game are either based on real-life league average proportions or sampled directly from the NFL dataset from 2013-2022.
- The original plan was to build a full-fledged regression model to predict the number of yards each play would gain, but there proved to be too little signal in the data. Thus, I pivoted to using the data as a distribution from which I would sample play results by situation.

## Current Functionality
- Game state displayed
- Restart game button
- Field position and line-to-gain indicated by lines and football on the field that move as the game state updates
- Clock that runs off a randomly generated number of seconds after each play call
- Buttons for: rushing, passing, punting, and kicking a field goal
- If a drive results in points, the score is updated
- At the end of a user drive, the user is prompted to sim cpu drive, and this then simulates a cpu drive result and runs off a game accurate amount of playclock
- Increased likelihood of CPU scoring after a Turnover on Downs or Missed Field Goal

## Functionality yet to be added
- ~~AT CURRENT STATE THE GAME NEVER ENDS! This is important to know for testing purposes. It will continue on to quarter 5, quarter 6, and so on.~~
- ~~Interceptions~~
- ~~Fumbles~~
- ~~Sacks~~
- Halftime ends the current drive
- ~~Coin Toss/User deciding whether to kick or receive at game start~~
- Align result messages to always be centered
- ~~Display Final Score at game end~~
