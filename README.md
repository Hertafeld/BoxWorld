# BoxWorld
A genetic algorithm which evolves creatures to grab falling boxes

Documentation is in progress, but for now feel free to simply run geneModule.py. 

The program creates and breeds agents whose goal is to collect as many falling "treats"
as possible in their short lifespan. These treats spawn randomly from the top
of the play area and fall at a constant rate. Agents can run left or right and jump.
As soon as a treat is collected, another spawns. This means it's to the agents' advantage
to collect the treats in the air.

Fitness, by default, is based on the number of treats collected. The more treats an agent collects,
the higher the chance of it breeding with other agents and producing children with similar behavior.

The simulation starts by initializing a number of new agents. Each agent has randomized DNA.
DNA is in the form of a table which provides an action (move left, move right, or jump)
for every possible situation (combination of horizontal distance from treat, vertical distance
from treat, and vertical velocity).

For example, the agent might be 5 units left of the treat, 8 units below it, and be moving upwards with speed 3.
If an agent has "left" as its DNA entry, it will move left every time it finds itself in this situation. In this way
the agents are deterministic, though their enviromnent (treat spawn locations) is random.

The default sim has a single-player world, 200 generations, a population of 100 agents, and a mutation rate of 1%.
Generally the best agent will figure out how to do a pretty good job of collecting most or all of the treats. It
will automatically show a replay of the best run of the best agent at the end of the sim.

The sim will also create a plot of the best and average fitnesses over time, as well as create replay files so that
you can watch the evolutoin of agents.

Running "replayViewer.py" will bring up a command-line style interface. Type the names of the replay files, surrounded by quotes,
to watch the replay. It can be fun to see how far those guys came from their early days!


Generally the "optimal" agent will be pretty predictible. To spice things up, you can run sims of multiple populations battling it out.
The "runCompetition" creates two populations. At each generation, every agent from one population "battles" every agent from the other.

This is where the fitness function comes into play. In a single-player sim, evaluating fitness by treats collected is the way to go. But
with two agents in the field, this decision is less trivial. Take a look at the code to see the different fitness functions you can use, 
or try writing your own! 

For example, if each agent is rewarded as in the single-player sim (number of treats collected), then agents will
be aggressive and box out the opponent. However, one could also evaluate fitness based on the sum collected by an agent and its opponent.
This would encourage agents to cooperate - in practice they often will stay in sync, each handling half of the board and allowing whoever
is closer to grab the treat. 

Another idea would be for both agents to be evaluate based on how many treats the red agent collects; that 
means the blue agent wants the red agent to get them all. Sometimes the blue will evolve to stay out of red's way, and under the right
conditions may even learn to allow red to jump on his head to collect the treat sooner!

Currently the sim isn't very accessible, and requires some code-digging to really customize the sim. 
Hopefully this will change in the future. Until then, happy simulating!
