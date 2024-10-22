import greedy
import random

# https://www.youtube.com/watch?v=4b5d3muPQmA&t=33s
# Good video about what clustering is


"""
Global variables:
nums = list of data points
X = cluster assignments; this is a list the SAME length as 'nums', and each value is randomly generated as being 0, 1 or 2
If the value is 0, then the value in 'nums' to the corresponding index will be assigned to cluster 1.
For example, if nums = [1.3, 2.7, 0.4] and X = [1, 0, 2] then '1.3' is assigned to cluster 2, '2,7' is assigned to 1, and 0.4 is assigned to 3
Cluster 1 = index 0
Cluster 2 = 1
Cluster 3 = 2 (These random assignments are made by making a random integer between 0 and K-1, which explains the offset of 1)

K = number of clusters (in the YouTube video, it explains why 3 is often the amount of clusters used to get best results)

R = number of iterations in the loop
"""


def cluster(nums,K,R):

    # Step 1. Initialization

    # Start with random cluster assignments
    N = len(nums)
    X = []
    for n in range(N):
        X = X + [random.randint(0,K-1)] # Randomly assigns a value of 0, 1 or 2 to X (currently an empty list)
    X = greedy.cluster_fix(X,K) # Applies the cluster_fix function from greedy.py (if a cluster does not have any assigned values,
    # it automatically appends the index number to it)
    n = 0
    while (n <= R): # R = 20, so the loop runs 20 times (or until the termination condition is met)

        # Step 2. Neighbourhood search and termination check

        # Compute current cluster objective
        μ = greedy.cluster_means(nums,X,K)
        # This finds the centroid of the cluster (the mean value of all of the date points in a given cluster)

        F = greedy.cluster_obj(nums,X,μ,K)
        # This calculates the objective function of any given cluster
        # It calculates the distance from each data point in the given cluster from the centroid of the cluster, and then add them all
        # up, so as to find the total cost of this cluster

        print(f'Iteration n={n}: assignments X={X}, objective F={F}')

        # Find (1-Hamming) neighbourhood of cluster assignments
        Xnbr = greedy.cluster_nbr(X,K)
        # For each data point in each cluster, it incrementally assigns one data point to the next cluster so that we can evaluate
        # different configurations and see if we are able to create a 'better' clustering (as we calculate in the function cluster_nbrobj)
        
        # This function returns n lists (n = amount of data points in a given cluster) with the different neighbouring configurations

        # Evaluate objective value of all cluster assignments in neighbourhood
        Fnbr = greedy.cluster_nbrobj(nums,Xnbr,K)
        # This function takes in as an argument all of the lists generated from the cluster_nbr() function, and finds the objective
        # function value (minimum values in this case) for each of the configurations


        # Select optimal assignment X in neighbourhood
        iopt,Fopt = greedy.mintuple(Fnbr)
        # This function takes in the different values generated by the neighbouring configurations, and finds the 'most optimal'
        # configuration generated by this

        # Check termination
        if Fopt >= F:
            break
        
        # F = the objective function of our given cluster
        # Fopt = the objective function of the neighbouring cluster that we have just evaluated
        # We are aiming to minimise this objective function: this means that if even our 'most optimal' neighbouring configuration
        # results in an increase of the objective function of our current cluster, it is counter-intuitive to calculate any new values
        # so we break the program and assume that we have found our local optima


        # Update assignments
        X = Xnbr[iopt]
        # X is updated with the best cluster configuration found in this iteration of the for loop, so that the next time the loop runs,
        # it can iterate again and incrementally improve again and again, until eventually it finds the local optima and breaks the loop

        # Step 3. Iterate
        n = n + 1
    
    return X,F

nums = [0.1,-0.3,2.6,1.1,2.3,-0.8,-6.2,-7.8,-1.5,-0.4]
print(f'Input data: nums={nums}')
K = 3 # Number of clusters
R = 20 # Number of iterations in the for loop
Xopt,Fopt = cluster(nums,K,R)
print(f'Greedy K-clustering: X*={Xopt}, F*={Fopt}')