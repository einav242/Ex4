# **Ex4** -  “Pokemon game”

![pokemon-logo](https://user-images.githubusercontent.com/93201414/148660272-da72a678-1964-4a83-8004-6bc1d0b8859d.jpeg)


### :pushpin:  “Pokemon game” -  in which given a weighted graph,  a set of “Agents” should be located on it so they could “catch” as many “Pokemons” as possible.
The pokemons are located on the graph’s (directed) edges, therefore, the agent needs to take (aka walk)  the proper edge to “grab” the pokemon
The goal is to maximize the overall sum of weights of the “grabbed” pokemons (while not exceeding the maximum amount of server calls allowed in a second - 10 max)
As part of this project, we can use a data structure and algorithms on graphs (oriented and weighted).

## The algoritm : 
The goal is for every agent to catch as many Pokemon as possible.
So we created an algorithm that works in such a way that we go through all the agents. 
And each agent places the Pokemon closest to him , taking into account which Pokemon rib sits on. 
In the edge function – we will check which Pokemon side sits on. 
And to know which Pokemon is best for the agent to catch (on the shortest route) 
Considered by the shortpath function the shortest route so that the agent can catch the Pokemon .


### How to Run The Game: 
To run our project you must open 2 CMD windows simultaneously from within the project 


### Thr Result:

| Case | Grade | Move | 
| ------- | ------- | ------- | 
| 0 | 100 | 298 |
| 1 | 327 | 596 |
| 2 | 207 | 298 |
| 3 | 611 | 596 |
| 4 | 249 | 298 |
| 5 | 488 | 596 |
| 6 | 79 | 298 |
| 7 | 269 | 596 |
| 8 | 100 | 298 |
| 9 | 294 | 596 |
| 10 | 140 | 298 |
| 11 | 628 | 495 |
| 12 | 40 | 298 |
| 13 | 204 | 596 |
| 14 | 173 | 289 |
| 15 | 269 | 585 |


### Example of Case 11: 
As you can see in the game, we can see the Pokemon on the game board and the agents who are aiming to catch Pokemon. 
On the bottom right we can see the time left for the end of the game and the scoring.
And a stop button if you want to stop the game in the middle. 

<img width="809" alt="Capture" src="https://user-images.githubusercontent.com/93201414/148661054-e71bb830-b930-47e6-81e8-ef6865ee0e67.PNG">




