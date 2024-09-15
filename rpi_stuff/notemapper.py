leftmost = 'D3'
notemapping = {}
curr = leftmost

for i in range(12):
	notemapping[curr] = i


	curr = chr(ord(curr[0])+1) + curr[1]
	if curr[0] == 'H':
		curr = 'A' + curr[1]
	if curr[0] == 'C':
		curr = curr[0] + str(int(curr[1])+1)
		
[print(i) for i in notemapping]
