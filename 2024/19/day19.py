from functools import cache
def is_design_possible(design, towel_patterns):
  if not design:
    return True 

  for pattern in towel_patterns:
    if design.startswith(pattern):
      if is_design_possible(design[len(pattern):], towel_patterns):
        return True
  return False

def count_possible_designs(towel_patterns, designs):

  count = 0
  for design in designs:
    if is_design_possible(design, towel_patterns):
      count += 1
  return count

if __name__ == "__main__":
  with open("day19.txt", "r") as file:
    towel_patterns = file.readline().strip().split(", ")
    designs = [line.strip() for line in file.readlines()[1:]]

  possible_designs = count_possible_designs(towel_patterns, designs)
  print(f"Number of possible designs: {possible_designs}")
  @cache
def count_rear_num(pattern):
    if len(pattern) == 0: return 1 # Base case
    return sum(count_rear_num(pattern[len(towel):]) for towel in towels if pattern.startswith(towel))

print(sum(count_rear_num(pattern) for pattern in patterns))
