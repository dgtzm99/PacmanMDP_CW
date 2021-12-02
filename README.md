# Pacman
King's College London Coursework for 6CCS3AIN (AI Reasoning and Decision Making)

To run pacman.py on David's windows 10
launch xming x server located in 'Program Files (x86) 
click on the 'XLaunch' file
now on the command line:

'export DISPLAY=localhost:0.0'
'python2 pacman.py'


Remember to disconnect the server when you are finished. 
That is navigate to the mini-icons on the down-right corner on the 
desktop, and click the xming 'exit'


///Playing with Random Agent
	'python2 pacman.py --pacman RandomAgent'
	'python2 pacman.py --pacman RandomishAgent'
	'python2 pacman.py --pacman SensingAgent'

	Made by me
	'python2 pacman.py --pacman GoWestAgent'
	'python2 pacman.py --pacman HungryAgent'
	'python2 pacman.py --pacman SurvivalAgent'

///Practical 2
	Corners of medium classic is: [(0, 0), (19, 0), (0, 10), (19, 10)]
	'python2 pacman.py --pacman CornerSeekingAgent --layout mediumClassicNoGhosts'

///Coursework
	Testing
	'python2 pacman.py --pacman MDPAgent'
	'python2 pacman.py -q -n 25 -p MDPAgent -l smallGrid'
	'python2 pacman.py -q -n 25 -p MDPAgent -l mediumClassic'




