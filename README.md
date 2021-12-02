# Pacman
King's College London Coursework for 6CCS3AIN (AI Reasoning and Decision Making)

This is a Coursework where one has to develope an agent that can calculate Markov Decision Process (MDP) using Value iteration to calculate the utilities throughout the space of the many pacman maps.

With the MDP, the agent (pacman) should be able to avoid ghosts, and win the game, that is, by finishing eating all the food and capsules before the ghosts get to pacman.

The Agent's success is not expected to be perfect. (~17/25 in smallGrid | ~8/25 in mediumClassic)

To run pacman.py on David's windows 10
launch xming x server located in 'Program Files (x86) 
click on the 'XLaunch' file
now on the command line:

'export DISPLAY=localhost:0.0'
'python2 pacman.py'


Remember to disconnect the server when you are finished. 
That is navigate to the mini-icons on the down-right corner on the 
desktop, and click the xming 'exit'


	Coursework testing commands
	'python2 pacman.py --pacman MDPAgent'
	'python2 pacman.py -q -n 25 -p MDPAgent -l smallGrid'
	'python2 pacman.py -q -n 25 -p MDPAgent -l mediumClassic'




