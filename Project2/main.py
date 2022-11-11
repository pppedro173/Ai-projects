import csp
import itertools


class Problem(csp.CSP):

	def __init__(self, fh):
		# Place here your code to load problem from opened file object fh and
		# set variables, domains, graph, and constraint_function accordingly
		self.upperbound=24 					
		self.conflits={}
		self.result={}
		variables=[]
		domains={}
		graph={}
		T=fh.readline().rstrip().split(' ')		#file read
		R=fh.readline().rstrip().split(' ')
		S=fh.readline().rstrip().split(' ')
		W=fh.readline().rstrip().split(' ')
		A=fh.readline().rstrip().split(' ')
		fh.close()
		T=[tuple(v) for v in [s.split(',') for s in T[1:]]]
		variables=W[1:]											
		for var in variables:
			domains[var]=list(itertools.product(T,R[1:]))
			graph[var]=W[1:W.index(var)]+W[W.index(var)+1:]
		A=[tuple(v) for v in [s.split(',') for s in A[1:]]]
		aux=[]
		for students in S[1:]:
			aux=[]
			for t in A:
				if t[0]==students:
					aux.append(t[1])
			if len(aux)!=1:
				for course in aux:
					self.conflits[course]=aux[0:aux.index(course)]+aux[aux.index(course)+1:]
			else:
				self.conflits[aux[0]]=[]
		constraints_function=self.constraints
		super().__init__(variables, domains, graph, constraints_function)
		
	def dump_solution(self, fh):
		# Place here your code to write solution to opened file object fh
		fh.write('\n'.join('{} {}'.format (key, ''.join('{} {}'.format (','.join(val[0]), val[1]))) for key, val in self.result.items()))

	def constraints(self,A,a,B,b):
		# function that defines the constraints
		A=tuple(A.split(','))
		B=tuple(B.split(','))
		#constraint 3
		if A[0]==B[0] and A[1]==B[1] and a[0][0]==b[0][0]:
			return False
		#constraint 1
		if a==b:
			return False
		#constrain 2
		if a[0]==b[0]:
			if A[0]==B[0]:
				return False
			if A[0] in self.conflits[B[0]]:
				return False
		# constraint para minimização
		if int(a[0][1])>self.upperbound or int(b[0][1])>self.upperbound:
			return False 
		return True
        
def solve(input_file, output_file):
	p = Problem(input_file)
	# Place here your code that calls function csp.backtracking_search(self, ...)
	# result=csp.backtracking_search(p)
	p.result=optimization(p,{})
	p.dump_solution(output_file)


def optimization(p, result):
	# Do the minimization calling backstrack_search with decraising upperbound constraint iteratively
	if result != {}:	#just for the frist case
		values=list(result.values())
		hour=[int(t[1]) for t in [item[0] for item in values]]
		p.upperbound=max(hour)-1
		p.curr_domains = None
		p.nassigns = 0
	new_result=csp.backtracking_search(p,csp.mrv,csp.lcv,csp.forward_checking)
	if new_result==None:
		return result
	else:
		return optimization(p, new_result)

# start_time = time.time()
input_file=open('input_file.txt', 'r')
output_file = open('output_file.txt','w')
solve(input_file, output_file)
# print("--- %s seconds ---" % (time.time() - start_time))