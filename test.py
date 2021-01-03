# import numpy as np
# ar1 = np.zeros((1, 7), dtype=int)
# np.put(ar1, [1, 5], [3])
# ar2 = np.zeros((2, 7), dtype=int)
# ar1 = np.concatenate((ar1, ar2))
# print(ar1)
# ar = [ 2, 3, 1, 0, 5]
# ar1 = [ (True,x,y) if y<x 
#         else (False,x,y) 
#         for x in ar 
#         for i,y in enumerate(ar)]
# print(ar1)
# import itertools
# com = [ [1,2], [4,6,7], [11, 13]]
# com = list(itertools.product(*com))
# print(com)

# def calculate_column_sum(col):
#     total = 0
#     for num in col:
#         total += num
#     return total
# ar1 = [2, 3, 4, 5, 6]
# ar2 = [0, 4, -1, 0, 10]
# ar = np.array([[2, 3, 4, 5, 6], [0, 4, -1, 0, 10]])
# # ar3 = np.apply_along_axis(calculate_column_sum, 0, ar)
# ar3 = np.sum(ar, 0)
# ar4 = [x*x for x in ar3]
# print(ar3, np.sum(ar))
# print(ar4, np.sum(ar4))
# ar[1] = np.zeros(5, dtype=int)
# print(ar)
import numpy as np
# ar = np.array([ [1,2,3], [3, 3, 3], [4, 3, 2], [0, 3, 7] ])
# ar1 = np.where(ar[:, 1] + 1 < ar[:, 2] + 1)
ar = np.array([])
ar1 = np.array([1,2,3])
ar = ar = np.append(ar1, ar)
print(ar1)