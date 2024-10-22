def bellman(nums):

    # Initialization
    sum_tracker = (0,0)
    # s[0] keeps track of maximum sum found so far, s[1] keeps track of current running sum

    subarray_tracker = ([],[])
    # X[0] represents the subarray with the maximum sum, X[1] is the subarray currently being evaluated

    # Iteration
    for i in nums:
        if 0 > (i + sum_tracker[1]): # checks if the current running sum is greater than zero
            # if it's less than zero, the value is reset and we begin a new subarray
            current_sum = 0
            current_subarray = []
        else:
            current_sum = i + sum_tracker[1] # Adds the number in 'nums' we are currently iterating over to the current running sum
            current_subarray = subarray_tracker[1] + [i] # Add the value in 'nums' we are currently iterating over to the current running subarray
            
        if current_sum > sum_tracker[0]: # If the sum of the current subarray we are evaluating it greater than the max found so far:
            subarray_tracker = (current_subarray, current_subarray) # Update the largest found subarray in X so far
            sum_tracker = (current_sum, current_sum) # Update the largest found sum in S so far
        else:
            subarray_tracker = (subarray_tracker[0], current_subarray) # Keep max subarray unchanged, but update current running subarray
            sum_tracker = (sum_tracker[0], current_sum) # Keep max sum unchanged, but update current running sum

    return (subarray_tracker, sum_tracker)

nums = [0.1,-0.3,2.6,9.1,-0.8]

subarrays, sums = bellman(nums)
# Remember that we are returning two tuples from this function, so if we print out the sum (using the default numbers), we will 
# get a tuple that look like this: (11.7, 10.899999999999999) - the first value is the maximum sum found, 
# the second value is the sum we got after we iterated on the final value in the list (final value was -0.8, which is why the current
# running sum is lower)

print(f'Bellman recursion optimal sum S={sums}, configuration X={subarrays}')

