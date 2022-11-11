import prof
from math import exp
import time


class State:
    """ Class State : Takes care of all the operations on State type variables . 
    
        
        Attributes:
            nextP: Next player to play in the given state.
            listP1: Dictionary of lists of points which stores the sets of player one.
            listP2: Dictionary of lists of points which stores the sets of player .
            listEmp: List wich stores all the empty points in the board at the given state.
            adj: Dictionary to store the adjancies of the various points which belong to the sets.
            draw: Draw flag.
    """

    def __init__(self):
        """Inits State class instances."""
        self.nextP=0
        self.listP1={}
        self.listP2={}
        self.listEmp=[]
        self.adj={}
        self.draw=False

       

    def printList(self, list):
        """ auxliary method for testing"""
        print("[", end=" ")
        for n in range(len(list)):
            list[n].printP()
        print("]")

    def addElemP1(self, p):
        """Adds a new piece to player one list"""
        flag=True; # 0- Isolated piece; 1-Piece within a set
        index=[] #Stores the indexes of the list that need to be removed at the end
        remove=False # flag to know if we need to remove something at the end
        if self.listP1=={}:
            p.head=1
            self.listP1[1]=[p]
        else:
            for point in self.adj[(p.x,p.y)][1]:
                if point.type==1:
                    if flag==False:
                        if index.count(point.head)==0:
                            self.listP1[index[0]].extend(self.listP1[point.head])    # Binds existent sets
                            index.append(point.head)
                            for x in self.listP1[point.head]:
                                x.head=index[0]
                                self.changeADJ(None,x,1)
                            remove=True
                    if flag==True:
                        self.listP1[point.head].append(p)
                        p.head=point.head
                        flag=False
                        index.append(point.head)                        
            if remove==True:
                for i in reversed(index[1::]):
                    del self.listP1[i]
            if flag==True:
                list_keys=list(self.listP1.keys())
                p.head=list_keys[-1]+1                     # If there is no adjacent set it creates a new set (new list)
                self.listP1[list_keys[-1]+1]=[p]

            

        

    def addElemP2(self, p):
        """Adds a new piece to player two list"""
        flag=True; # 0- Isolated piece; 1-Piece within a set
        index=[] #Stores the indexes of the list that need to be removed at the end
        remove=False # flag to know if we need to remove something at the end
        if self.listP2=={}:
            p.head=1
            self.listP2[1]=[p]
        else:
            for point in self.adj[(p.x,p.y)][1]: 
                if point.type==2:
                    if flag==False:
                        if index.count(point.head)==0:
                            self.listP2[index[0]].extend(self.listP2[point.head])    # Binds existent sets
                            index.append(point.head)
                            for x in self.listP2[point.head]:
                                x.head=index[0]
                                self.changeADJ(None,x,1)
                            remove=True
                    if flag==True:
                        self.listP2[point.head].append(p)
                        p.head=point.head
                        flag=False
                        index.append(point.head)                        
            if remove==True:
                for i in reversed(index[1::]):
                    del self.listP2[i]
            if flag==True:
                list_keys=list(self.listP2.keys())                             
                p.head=list_keys[-1]+1                  # If there is no adjacent set it creates a new set (new list)                                  
                self.listP2[list_keys[-1]+1]=[p]
        
    def printState(self):
        """auxiliary test function to see if the states were correct"""
        print("Player:", self.nextP)
        print("Lugares vazios: ", end="")
        self.printList(self.listEmp)
        for key, values in self.listP1.items():
            print("P1: ", end=" ")
            print(values)
        for key, values in self.listP2.items(): 
            print("P2: ", end=" ")
            print(values)

    def createADJ(self, N):
        """Iterates trough all the columns and lines of the board and analyses each point individually"""
        for i in range(N):                                                
            for j in range(N):
                aux=[]
                if i>0:                          #norte
                    aux.append(Point(i,j+1))
                if j<N-1:                        #este
                    aux.append(Point(i+1,j+2))
                if i<N-1:                        #sul
                    aux.append(Point(i+2,j+1))
                if j>0:                        #oeste
                    aux.append(Point(i+1,j))
                self.adj[(i+1,j+1)]=[len(aux),aux]


    def changeADJ(self, t, p, flag=0):
        """ Changes the adjacencies"""
        for values in self.adj[(p.x,p.y)][1]:
            ind=self.adj[(values.getX(),values.getY())][1].index(p)
            self.adj[(values.getX(),values.getY())][1][ind].head=p.head
            if flag==0:
                self.adj[(values.getX(),values.getY())][1][ind].type=t
                self.adj[(values.getX(),values.getY())][0]=self.adj[(values.getX(),values.getY())][0]-1                        


    def getLiberties(self, lista):
        """ Returns the liberties of a set"""
        n_emp=0
        for p in lista:
            n_emp=n_emp+self.adj[p.x,p.y][0]
        return n_emp
  
                        
    def evalNeighbourHead(self,neighbour,state):
        """ Auxiliary method to evaluate the liberties of a set"""
        if(self.nextP==1):
            if(state==1):
                return self.getLiberties(self.listP1[neighbour.head])
            else:
                return self.getLiberties(self.listP2[neighbour.head])
        
        if(self.nextP==2):
            if(state==1):
                return self.getLiberties(self.listP2[neighbour.head])
            else:
                return self.getLiberties(self.listP1[neighbour.head])    
        
        
    def validActionsFunc(self,previousP):
        """ Returns the valid actions for a target player"""
        validActions = []
        stop=0
        for point in self.listEmp:
            for neighbour in self.adj[(point.getX(),point.getY())][1]:
                if neighbour.type == 0 :
                    validActions.append((self.nextP,point.getX(),point.getY()))
                    break
                if neighbour.type==self.nextP:
                    stop=0
                    if self.evalNeighbourHead(neighbour,1)!=1:
                        validActions.append((self.nextP,point.getX(),point.getY()))
                        stop=1
                        break
                    if stop==1:
                        break
                if neighbour.type==previousP: # 2 para player 1 e 1 para player 2
                    stop=0
                    if self.evalNeighbourHead(neighbour,0)==1:
                        validActions.append((self.nextP,point.getX(),point.getY()))
                        stop=1
                        break
                    if stop==1:
                        break
        return validActions


    def copy_state(self):
        """ Method to perform a copy of a state"""
        aux=[]
        out=State()
        out.nextP=self.nextP;
        for key,values in self.listP1.items():
                out.listP1[key]=values.copy()
        for key,values in self.listP2.items():
                out.listP2[key]=values.copy()
        for key,values in self.adj.items():
            aux=[]
            for point in values[1]:
                aux.append(point.copy_point())
            out.adj[key]=[values[0],aux]
        out.listEmp=self.listEmp.copy()
        out.draw=self.draw
        return out


    def evaluateAction(self, a):
        """Auxiliary method to organize actions"""
        if self.adj[(a[1], a[2])][0]==len(self.adj[(a[1], a[2])][1]):
            return -1
        else:
            return len(self.adj[(a[1], a[2])][1])-self.adj[(a[1], a[2])][0]
    
    def intermediateEvaluation(self,p):
        """ Evaluation of a non terminal state"""
        P1_liberties=[] # freedom degrees of player 1 
        P2_liberties=[] # freedom degrees of player 2
        for key,values in self.listP1.items():
            P1_liberties.append(self.getLiberties(values))
        for key,values in self.listP2.items():
            P2_liberties.append(self.getLiberties(values))
        if p==1:
            x=min(P1_liberties)-min(P2_liberties)+(sum(P1_liberties)-sum(P2_liberties))
        else:
            x=min(P1_liberties)-min(P2_liberties)+(sum(P2_liberties)-sum(P1_liberties))
        return x
    
    
    def terminalEvaluation(self,p):
        """ Returns the evaluation according to the player who lost the game"""
        for key,values in self.listP1.items():
            n_liberties=self.getLiberties(values)
            if n_liberties==0:
                if p==1:
                    return -1
                else:
                    return 1
        for key,values in self.listP2.items():
            n_liberties=self.getLiberties(values)
            if n_liberties==0: 
                if p==2:
                    return -1 
                else:
                    return 1
                
    def spaceLists(self,N,board):
        """ Creates tree list which are used to define the "game space" """
        for i in range(N):                               #Iterates trough all columns and lines of the board and analyses each point individually
            for j in range(N):
                # print(self.adj.get((i+1,j+1)))            #0-north/1-eeast/2-south/3-west
                if board[i][j]==0:
                    self.listEmp.append(Point(i+1,j+1))    # Creation of an empty space list --- it's added one to correct the coordinates
                elif board[i][j]==1:
                    p=Point(i+1,j+1)
                    self.addElemP1(p)
                    self.changeADJ(1,p)
                else:
                    p=Point(i+1,j+1)
                    self.addElemP2(p)
                    self.changeADJ(2,p)
            
        


class Point:
    """ Class Point : This clased is used to create point instances ,handle the copy of their data and easily get their
                      attributes. 
    
        
        Attributes:
            x: X coordinate of the point in question.
            y:  Y coordinate of the point in question.
            type: Point type. type=0-> empty space , type=1-> player one point , type=2-> player two point.
            head: Head of the set to which the point belongs. 

    """


    def __init__(self, x, y):
        """Initiates a Point with default coordinates ,type and head to be assigned later."""
        self.x=x
        self.y=y
        self.type=0
        self.head=0

    def __eq__(self,other):
        """ Equals function to compare the coordinates of points"""
        return self.x==other.x and self.y==other.y

    def __ne__(self,other):
        """ Complementary equals function"""
        return self.x!=other.x and self.y!=other.y

    def __repr__(self):
        """ Auxiliary function to print point coordinates and head in a aesthetic manner"""
        return "(%d,%d)--head:%d" % (self.x,self.y,self.head)


    def getX(self):
        """ retrieves the X coordinate of a point"""
        return self.x


    def getY(self):
        """ retrieves the Y coordinate of a point"""
        return self.y

    def printP(self):
        """ Auxiliary function to print point coordinates in the (x,y) format"""
        print("(%d,%d)" % (self.x,self.y), end=" ")

    def copy_point(self):
        """ Function that performs the copy of a point"""
        out=Point(0,0)
        out.x=self.x
        out.y=self.y
        out.type=self.type
        out.head=self.head
        return out





class Game:     
    """ Class Game : Main class of the program , handles all the major operations that feed the algorithm which
                    finds the best move to play.
    
        
        Attributes:
            None
    """
        

    def to_move(self, s):
        """Returns the player to move next given the state s"""
        return s.nextP
    

    def terminal_test(self,s):
        """Returns a boolean of whether state s is terminal or not"""
        if s.listEmp==[]:
            return True
        if s.draw==True:
            return True
        if s.listP1=={}:
            return False
        for key ,values in s.listP1.items():
            n_liberties=s.getLiberties(values)
            if n_liberties==0:
                return True
        if s.listP2=={}:
            return False
        for key,values in s.listP2.items():
            n_liberties=s.getLiberties(values)
            if n_liberties==0:
                return True
        return False



    def utility(self,s, p):
        """Returns the payoff of state s if it is terminal (1 if p wins, -1 if p loses, 0 in case of a draw), otherwise,
           its evaluation with respect to player p"""
        if self.terminal_test(s):
            if s.draw==True:
                return 0 # if the given state is a draw
            return s.terminalEvaluation(p) # Returns the evaluation according to which player lost
        else:
            x=s.intermediateEvaluation(p) # Returns and intermediate evaluation in the case of noone lossing
            return 2/(1+exp(-x))-1 # Mathematical function which bounds the evaluation to the interval [-1,1]
            

    def actions(self, s):
        """Returns a list of valid moves at state s"""
        validActions = []
        previousP=1
        if s.nextP==1:
            previousP=2
        validActions = s.validActionsFunc(previousP)
        if validActions==[]:
            s.draw=True                  
        return sorted(validActions, key=lambda n: self.utility(self.result(s,n),s.nextP),reverse=True)

    

    def result(self, s, a):
        """Returns the sucessor game state after playing move a at state s"""
        aux=s.copy_state()
        if a[0]==1:
            aux.nextP=2
            p=Point(a[1],a[2])
            aux.listEmp.remove(p) # Removes from the empty points list
            aux.addElemP1(p) # Adds a point to player one list
            aux.changeADJ(1,p) # changes adjacencies
        else:
            aux.nextP=1
            p=Point(a[1],a[2])
            aux.listEmp.remove(p) # Removes from the empty points list
            aux.addElemP2(p) # Adds a point to player two list
            aux.changeADJ(2,p) # changes adjacencies
        return aux



    def load_board(self, file):
        """Loads a board from an opened file stream s"""
        l=file.readline();                              #le a primeira linha do ficheiro
        N=int(l[0])
        s=State()
        s.nextP=int(l[2])
        board=[]
        for line in file:
            row=[0]*N
            for i in range(N):
                row[i]=int(line[i])
            board.append(row)
        s.createADJ(N)
        s.spaceLists(N,board)        
        return s



    """ Test miscellaneous"""

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)
        

    
    

        
        
        
start_time = time.time()
path='C:/Users/Pedro/Desktop/Ai/map.txt'
file=open(path, 'r')
game=Game()
Std=game.load_board(file)
game.initial=Std
print("JOGADA:", prof.alphabeta_cutoff_search(Std, game ))
print("--- %s seconds ---" % (time.time() - start_time))
print("--- %s seconds ---" % (time.time() - start_time))


