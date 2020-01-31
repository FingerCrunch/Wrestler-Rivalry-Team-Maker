# Wrestler-Rivalry-Team-Maker

This program solves the following problem:

There are two types of wrestlers: “Babyfaces” and “Heels”. There may or may not be a rivalry between any pair of wrestlers.  Suppose we have n wrestlers and a list of r pairs of rivalries. Find an efficient algorithm to determine whether two teams of wrestlers ("Babyfaces" and "Heels") can be formed such that each rivalry is only between a Babyface and a Heel. 

The program solves the problem in the following way:

This program creates a graph (represented by an adjacency list) where each vertex represents a wrestler and each edge represents a rivalry.
It then performs Breadth First Search to determine the distance of each vertex from the first wrestler given. The wrestlers will be assigned teams based on distance from the starting vertex. If the distance from the starting distance is even, then that vertex is on the same team as the starting vertex (Babyfaces); whereas, if that vertex is odd, then that vertex is on the opposing team (Heels).

