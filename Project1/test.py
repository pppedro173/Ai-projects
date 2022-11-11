path='C:/Users/clcas/Desktop/AI/map.txt'
file=open(path, 'r')
l=file.readline();
N=int(l[0])
fristP=l[2]
print(N)
board=[]
for line in file:
	row=[0]*N
	for i in range(N):
		row[i]=line[i]
	board.append(row)
print(board)



