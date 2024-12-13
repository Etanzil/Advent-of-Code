with open('day12.txt', 'r') as file:
    field = [row for row in file.read().splitlines()]
 
regions = {}
 
last_row = [(0,len(field[0]),'',None)]
for row_ind, row in enumerate(field):
    last_i, last_j, last_crop, last_reg = last_row.pop(0)
    this_row = []
    i = 0
    ids_to_merge = {}
    
    while i < len(row):
        reg = None
        crop = row[i]
        j = i + 1
        while j < len(row) and row[j] == crop:
            j += 1
        
        if last_j > i and last_crop == crop:
            reg = last_reg
            regions[reg][0] += j-i
            if i != last_i:
                regions[reg][1] += 2
            if j != last_j:
                regions[reg][1] += 2
 
        while last_j < j:
            last_i, last_j, last_crop, last_reg = last_row.pop(0)
            
            if last_j <= i:
                continue
            
            if last_crop == crop:
                if not reg:
                    reg = last_reg
                    regions[reg][0] += j-i
                    if i != last_i:
                        regions[reg][1] += 2
                    if j != last_j:
                        regions[reg][1] += 2
                elif reg != last_reg:
                    if reg in ids_to_merge:
                        if last_reg not in ids_to_merge[reg]:
                            ids_to_merge[reg].append(last_reg)
                    else:
                        ids_to_merge[reg] = [last_reg]
                    last_reg = reg
                    if j == last_j:
                        regions[reg][1] -= 2
                elif j == last_j:
                    regions[reg][1] -= 2
 
        if not reg:
            reg = f'{row_ind}{crop}{i}'
            regions[reg] = [j-i, 4]
        
        this_row.append((i,j,crop,reg))
        i = j
 
    for keep_id in ids_to_merge:
        while ids_to_merge[keep_id]:
            del_id = ids_to_merge[keep_id].pop(0)
            if del_id in ids_to_merge:
                ids_to_merge[keep_id] += ids_to_merge[del_id]
                ids_to_merge[del_id] = []
            regions[keep_id][0] += regions[del_id][0]
            regions[keep_id][1] += regions[del_id][1]
            del regions[del_id]
    
    last_row = this_row
    
cost = 0
for _, (area, edges) in regions.items():
    cost += area * edges
 
print(cost)
