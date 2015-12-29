########################################
########################################
############## MINESWEEPER #############
########################################
########################################
######### Python Version 2.7.10 ########
########################################
########################################

I. Download the MiniSAT solver. Details on installation and usage can be found at: http://minisat.se/MiniSat.html
II. Input: A plaintext file describing the layout - The first line of the file are the number of rows and columns respectively. Each following line corresponds to the cells of a row starting with the topmost row. Cells in a row are separated by commas. For example, the board configuration - 
	1 2 2 1 0
	1 X X 1 0
	1 2 2 1 0
will be given as - 
	3 5
	1,2,2,1,0
	1,X,X,1,0
	1,2,2,1,0
III. Output: A file of CNF constraints (in the specified format) to feed to the solver.
IV. Usage: Use the command 'python convert2CNF.py input.txt cnf.txt' to create the CNF constraints from a given board configuration. Then use the command 'minisat cnf.txt output.txt' to use the SAT solver to solve the CNF constraints.
