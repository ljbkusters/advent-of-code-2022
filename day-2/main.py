import rps_module
import numpy

# load data
data = numpy.genfromtxt("data.txt", delimiter=" ", dtype=str)

# calculate score
scores = [rps_module.round_score_calculator(a, b)
          for (a, b) in data]

# print answer
print("part 1:")
print(sum(scores))

# calculate score
scores = [rps_module.strategy_score_calculator(a, b)
          for (a, b) in data]
print("part 2:")
print(sum(scores))