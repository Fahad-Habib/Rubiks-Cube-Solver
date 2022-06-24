from pprint import pprint
from cube import Cube

c = Cube()
c.generate_random_cube()
print("Random Cube\n")
pprint(c.cube)
c.solve()
print("\nSolved Cube\n")
pprint(c.cube)
