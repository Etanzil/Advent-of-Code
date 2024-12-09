def parse_input(filename):
    with open(filename, 'r') as f:
        sections = f.read().strip().split('\n\n')
    
    rules = [tuple(map(int, line.split('|'))) for line in sections[0].splitlines()]
    updates = [list(map(int, line.split(','))) for line in sections[1].splitlines()]
    
    return rules, updates

def is_order_correct(update, rules):
    for x, y in rules:
        if x in update and y in update:
            if update.index(x) > update.index(y):
                return False
    return True

def reorder_update(update, rules):
    # Generate a dependency graph
    from collections import defaultdict, deque

    graph = defaultdict(list)
    indegree = defaultdict(int)
    pages = set(update)

    for x, y in rules:
        if x in pages and y in pages:
            graph[x].append(y)
            indegree[y] += 1

    # Perform topological sort
    sorted_update = []
    queue = deque([page for page in pages if indegree[page] == 0])

    while queue:
        current = queue.popleft()
        sorted_update.append(current)

        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_update

def find_middle_sum(filename):
    rules, updates = parse_input(filename)
    
    correctly_ordered_updates = []
    incorrectly_ordered_updates = []

    for update in updates:
        if is_order_correct(update, rules):
            correctly_ordered_updates.append(update)
        else:
            incorrectly_ordered_updates.append(update)
    
    # Sum of middle pages for correctly ordered updates
    middle_sum_correct = sum(
        update[len(update) // 2] for update in correctly_ordered_updates
    )

    # Reorder the incorrectly ordered updates
    reordered_updates = [reorder_update(update, rules) for update in incorrectly_ordered_updates]

    # Sum of middle pages for reordered updates
    middle_sum_incorrect = sum(
        update[len(update) // 2] for update in reordered_updates
    )

    return middle_sum_correct, middle_sum_incorrect

if __name__ == "__main__":
    filename = "day5.txt"
    part_one, part_two = find_middle_sum(filename)
    print(f"Part One: The sum of the middle page numbers from correctly ordered updates is: {part_one}")
    print(f"Part Two: The sum of the middle page numbers after reordering incorrectly ordered updates is: {part_two}")
