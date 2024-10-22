import math

# Find minimum of list of tuples
def mintuple(x):
    xmin = math.inf
    for i,xp in x:
        if xp < xmin:
            imin,xmin = i,xp
    return (imin,xmin)

# Ensure cluster assignment is feasible (has at least one data point in each cluster)
def cluster_fix(X,K):
    """
    cluster_assignments = the integer values associated with each cluster
    number_of_clusters = list of clusters
    This function ensures that every cluster has at least one data point assigned to it (otherwise the other functions would break)
    For example, if cluster 2 doesn't have any data points, starting on the 0th index, we would add the value '1' to the cluster.
    If cluster 3 doesn't have any data points, then we would add the value '2' to the cluster.
    As far as I can tell, this is just for the sake of demonstration and isn't actually done like this in real life
    """
    N = len(X) # I don't think this actually does anything
    for k in range(K):
        if X.count(k) == 0: # if the second value in the tuple is empty:
            X[k] = k # append the current idex 'k' to the tuple
    return X  

# Cluster means
def cluster_means(x,X,K):
    """
    This returns the mean value of a cluster; if the cluster has the values [1, 3] assigned to it, the centroid of the function would be
    2, and this would be how we can calculate the distance of each data point from the centroid.
    (I think this becomes more important when we start calculating neighbouring configurations and calculating how the space from 
    the centroid changes)
    """
    N = len(X)
    mu = [0]*K
    for k in range(K):
        xk = [x[i] for i in range(N) if X[i]==k]
        # This line creates a list of data points assigned to the given cluster:
        # x = list of data points (for all clusters)
        # x[i] for i in range(N) = iteration over every data point in the list
        # big 'X' = list that maps data points to clusters (with three clusters, it would look like [0, 2, 1, 2, 0, 1, 1, 0] etc)
        # 'if X[i]==k' means that only data points from a given cluster are appended to the list
        # if we are looking at the first cluster, this list would only look at the '0's, and append all the data points that correspond
        # to those indexes

        mu[k] = sum(xk)/len(xk)
    return mu

# Compute cluster objective
def cluster_obj(x,X,mu,K):
    """
    The returns the objective function of a cluster (ojective function is to minimise or maximise the result- here, we aim to 
    minimise the distance of the sum of all the data points from the centroid of a cluster)
    """
    N = len(X)
    F = 0 # The objective function is initialised as 0
    for k in range(K):
        xk = [x[i] for i in range(N) if X[i]==k]
        # Same list comprehension as in cluster_means(); maps all the data points from our current cluster into a list
        dk = sum([(xp-mu[k]/len(xk))**2.0 for xp in xk])
        # xp = every value iterated over in the list 'xk' that we just created last line
        # we find the sum of xp minus the mean value 'mu' (the centroid value that we calculated in the previous function) divided
        # by the length of the amount of data points in the cluster, to the power of 2 (**2 = to the power of 2)
        F = F + dk
    return F

# Create 1-Hamming distance cluster assignment neighbourhood
def cluster_nbr(X,K):
    """
    The function incrementally moves data points, one by one, to the neighbouring cluster, so that it can calculate how the objective
    function changes in a later function, and determine whether there is a more optimal configuration of clustering than the one
    currently being evaluated.
    This returns the list 'Xnbr' of the different configurations generated by shifting different data points into neighbouring clusters
    """
    N = len(X)
    Xnbr = []
    for n in range(N):
        j = X[n] + 1 # X = list of cluster assignments, so if a data point is assigned to cluster 1, that piece of data will now be assigned
        # to cluster 2, and so forth
        if j == K:
            j = 0
        Xn = X.copy() # This creates a copy of the original cluster assignment so we don't overwrite the original values permanently
        Xn[n] = j # The cluster assignment at index 'n', is assigned the new value 'j' which was initialised earlier in this function
        Xnbr = Xnbr + [cluster_fix(Xn,K)]
    return Xnbr

# Evaluate objectives for cluster assignment neighbourhood
def cluster_nbrobj(x,Xnbr,K):
    """
    This takes in the list 'Xnbr' which we generated from the previous function, and finds the objective function value of each
    of these neighbouring configurations, then returns the list 'Fnbr' (in the K-Clustering.py file, this list will be fed into the
    min_tuple() function to find the best configuration, i.e. the one with the lowest cost value)
    """
    N = len(x)
    Fnbr = []
    for nbr in range(N):
        mu = cluster_means(x,Xnbr[nbr],K)
        Fnbr = Fnbr + [(nbr,cluster_obj(x,Xnbr[nbr],mu,K))]
    return Fnbr