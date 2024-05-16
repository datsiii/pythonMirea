def bucketsort(arr, k):
    """
   Sorts the input array using bucket sort algorithm.

   Parameters:
   arr (list): Input array to be sorted
   k (int): Range of the input array elements

   Returns:
   list: Sorted array

   Examples:
   >>> bucketsort([3, 2, 6, 1, 4, 5], 7)
   [1, 2, 3, 4, 5, 6]
   >>> bucketsort([5, 4, 3, 2, 1, 0], 6)
   [0, 1, 2, 3, 4, 5]
   >>> bucketsort([1], 1)
   [1]
   """
    if k <= 0:
        raise ValueError("Value of k should be greater than 0")

    counts = [0] * k
    for x in arr:
        if x < 0 or x >= k:
            raise ValueError("Elements in arr should be in the range of 0 to k-1")
        counts[x] += 1

    sorted_arr = []
    for i in range(k):
        sorted_arr.extend([i] * counts[i])

    return sorted_arr
