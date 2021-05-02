import random
import time
import os


g=1
class point():
    """
    makes a point with x and y coordinate

    args: constructor take arguments: x and y coordinates

    """


    def __init__(self,x,y):

        """

        :param x: x coordinate of point
        :param y: y coordinate of point
        """
        self.x=x
        self.y=y




class grid():

    """
    does functions related to grid

    data members:
    a. N : size of the grid
    b. start : original position of the player
    c. goal: final position of the player
    d. myObstacles: an array of obstacles
    e. myRewards: an array of rewards

    functions:
    rotateClockwise(n) : rotates the grid clockwise n times by 90
    rotateAnticlockwise(n) : rotates the grid anti-clockwise n times by 90
    showgrid():prints grid on console.
               representation: obstacles = #
                               rewards = by their value
                               empty cells = *
                               player = ^O^
    and helper functions

    """



    def __init__(self,n=36):
        """

        :param n: grid length

        """
        self.N=n
        self.grid=self.make_grid()




    def make_grid(self):

        #comma htaya
        """

        HELPER FUNCTION
        makes grid with a boundary and empty cells represented by *
        calls helper functions to spawn rewards and obstacles
        :return: the grid it made


        """


        grid = []
        for x in range(0, self.N + 2):
            if x == 0 or x == self.N + 1:
                grid = grid +[[" !-"] + ["---"] * (self.N) + ["-! "]]
            else:
                grid += [[" | "] + [" * "] * self.N + [" | "]]
        #print(grid)
        grid=self.make_entry(grid)
        grid = self.make_exit(grid)
        self.myObstacles=self.make_obstacle()
        grid=self.put_obstacles_on_grid(grid,self.myObstacles)

        self.myRewards=self.make_reward(grid)
        grid=self.put_rewards_on_grid(grid,self.myRewards)

        #self.show_grid(grid)
        return grid




    def make_entry(self,grid):


        """

        HELPER FUNCTION
        MAKES ENTRY POINT AT BOUNDARY
        :param grid: takes input grid for which it makes entry point at random
        :return: grid with entry point


        """


        a=random.randint(1, 2 * self.N - 1)
        if 0<a<self.N//2:
            grid[0][a]=" S "
            self.start=point(a,1)
            self.position=point(a,1)

        elif self.N//2<=a<self.N:
            grid[self.N + 1][a - self.N // 2 + 1]= " S "
            self.start=point(a - self.N // 2 + 1, self.N)
            self.position=point(a - self.N // 2 + 1, self.N)

        elif self.N<=a<2*self.N:
            grid[a - self.N + 1][0]= " S "
            self.start=point(1, a - self.N + 1)
            self.position=point(1, a - self.N + 1)                         #hidden

        return grid




    def make_exit(self,grid):


        """


        HELPER FUNCTION
        MAKES EXIT POINT AT BOUNDARY
        :param grid: grid for which it makes exit point at boundary
        :return: grid with exit point


        """


        a = random.randint(1, 2 * self.N - 1)
        if 0 < a < self.N // 2:
            grid[0][a + self.N // 2] = " E "
            self.goal=point(a + self.N // 2, 1)
        elif self.N // 2 <= a < self.N:
            grid[self.N + 1][a] = " E "
            self.goal=point(a, self.N)
        elif self.N <= a < 2 * self.N:
            grid[a - self.N + 1][-1] = " E "
            self.goal=point(self.N, a - self.N + 1)
        return grid



    def make_obstacle(self):


        """


        HELPER FUNCTION
        makes obstacles at random co-ordinates
        :return: list of co-ordinates of randomly spawned obstacles


        """

        if self.N>=5:
            a=random.randint(self.N // 2, 2 * self.N)
        else:
            a= random.randint(self.N // 2,self.N)
        Obstacles=[]
        z=0
        while z<a:
            b=random.randint(1, self.N)
            c = random.randint(1, self.N)
            if self.start!=point(b,c) and self.goal!=point(b,c):
                if (self.start.x-b)+(self.start.y-c)!=1 and (self.goal.x-b)+(self.goal.y-c)!=1:
                    Obstacles=Obstacles+[Obstacle(b,c)]
                    z=z+1
        return Obstacles



    def put_obstacles_on_grid(self,grid,obstacles):

        """


        HELPER FUNCTION
        puts obstacles on the grid
        :param grid: grid on which obstacles are to be put
        :param obstacles: list of obstacles made by make_obstacle
        :return: grid with obstacles


        """
        for var in obstacles:
            grid[var.y][var.x]=" # "
        return grid




    def make_reward(self,grid):

        """

        HELPER FUNCTION
        makes list of coordinates of rewards that are to be spawned randomly
        :param grid: grid for which it makesrandomly spawned rewards
        :return: list of randomly spawned rewards

        """

        if self.N>=5:
            a=random.randint(self.N // 2, 2 * self.N)
        else:
            a= random.randint(self.N // 2,self.N)
        rewards=[]
        z=0
        while z<a:
            b=random.randint(1, self.N)
            c = random.randint(1, self.N)
            if self.start!=point(b,c) and self.goal!=point(b,c):
                if (self.start.x-b)+(self.start.y-c)!=1 and (self.goal.x-b)+(self.goal.y-c)!=1:
                    if grid[c][b]!=" # ":
                        #print(grid[c][b])
                        rewards+=[Reward(b,c)]
                        z=z+1
        return rewards




    def put_rewards_on_grid(self,grid,rewards):

        """

        HELPER FUNCTION
        puts rewards on grid
        :param grid: grid on which it spawns rewards
        :param rewards: list of coordinates of rewards
        :return: grid having randomly spawned rewards

        """

        for var in rewards:
            grid[var.y][var.x]=" "+str(var.value)+" "
        return grid




    def upgrade_grid(self,move):

        """

        HELPER FUNCTION
        upgrades grid according to players input and moves
        :param move: determines where the player wants to take its character
        :return: decrease in energy of player according to moves

        """

        self.grid[self.position.y][self.position.x]=" X "
        #self.position.x=px
        #self.position.y=py
        #self.show_grid(self.grid,px,py)
        z=-1

        if move=="L":
            a = []
            for x in range(1, self.N + 1):
                a += [x]
            if self.position.x == 1 and self.position.y in a:
                self.position.x = self.N
            else:
                self.position.x-=1
            if self.grid[self.position.y][self.position.x]==" # ":
                z=-(4*self.N)
            elif self.grid[self.position.y][self.position.x]==" * ":
                z=-1
            elif self.grid[self.position.y][self.position.x]==" X ":
                z=-1
            else:
                z=int(self.grid[self.position.y][self.position.x].strip())*self.N

            #clear()
            self.show_grid(self.grid,self.position.x,self.position.y)
            #time.sleep(g)
            if self.position.x==self.goal.x and self.position.y==self.goal.y:
                print("*"*90+"!!!!!!!!!!YOU WON !!!!!!!!!!! "+"*"*90)
                exit()
            return z


        if move=="R":
            a = []
            for x in range(1, self.N + 1):
                a += [x]
            if self.position.x == self.N and self.position.y in a:
                self.position.x = 1
            else:
                self.position.x+=1
            if self.grid[self.position.y][self.position.x]==" # ":
                z=-(4*self.N)
            elif self.grid[self.position.y][self.position.x]==" * ":
                z=-1
            elif self.grid[self.position.y][self.position.x]==" X ":
                z=-1
            else:
                z=int(self.grid[self.position.y][self.position.x].strip())*self.N
            #clear()
            self.show_grid(self.grid,self.position.x,self.position.y)
            #time.sleep(g)
            if self.position.x==self.goal.x and self.position.y==self.goal.y:
                print("*"*90+"!!!!!!!!!YOU WON !!!!!!!!!!!"+"*"*90)
                exit()
            return z

        if move=="U":
            a = []
            for x in range(1, self.N + 1):
                a += [x]
            if self.position.y == 1 and self.position.x in a:
                self.position.y = self.N
            else:
                self.position.y-=1
            if self.grid[self.position.y][self.position.x]==" # ":
                z=-(4*self.N)
            elif self.grid[self.position.y][self.position.x]==" * ":
                z=-1
            elif self.grid[self.position.y][self.position.x]==" X ":
                z=-1
            else:
                z=int(self.grid[self.position.y][self.position.x].strip())*self.N
            #clear()
            self.show_grid(self.grid,self.position.x,self.position.y)
            #time.sleep(g)
            if self.position.x==self.goal.x and self.position.y==self.goal.y:
                print("*"*90+"!!!!!!!!!!!!YOU WON !!!!!!!!!!! "+"*"*90)
                exit()
            return z


        if move=="D":
            a = []
            for x in range(1, self.N + 1):
                a += [x]
            if self.position.y == self.N and self.position.x in a:
                self.position.y = 1
            else:
                self.position.y+=1
            if self.grid[self.position.y][self.position.x]==" # ":
                z=-(4*self.N)
            elif self.grid[self.position.y][self.position.x]==" * ":
                z=-1
            elif self.grid[self.position.y][self.position.x]==" X ":
                z=-1
            else:
                z=int(self.grid[self.position.y][self.position.x].strip())*self.N
            #clear()
            self.show_grid(self.grid,self.position.x,self.position.y)
            #time.sleep(g)
            if self.position.x==self.goal.x and self.position.y==self.goal.y:
                print("*"*90+"!!!!!!!!!!YOU WON !!!!!!!!!!"+"*"*90)
                exit()
            return z




    def show_grid(self,grid,px,py):                               #earlier no position,griddddddd


        """
        *************************************************MAIN FUNCTION**************************************************
        :param grid: grid it needs to display
        :param px: player position x-coordinate
        :param py: player position y-coordinate
        :return: None, prints grid on console


        """

        for x in range(0, self.N + 2):
            for y in range(0, self.N + 2):
                if (x,y)==(py,px):                         #earlier self.position
                    print("^O^",end="")
                else:
                    print(grid[x][y], end="")
            print(" ")



    def rotateClockwise(self,m):

        """

        ******************************************************MAIN FUNCTION*********************************************
        turns grid clockwise by 90 degrees by m times
        :param m: no. of times a function is to be done
        :return: decrease in energy caused by the move

        """

        gridcopy=self.grid.copy()
        listgrids=[]


        z=0
        while z<m:
            new_grid=[]

            for x in range(1, self.N + 1):
                row=[]
                for y in range(1, self.N + 1):
                    row=row+[gridcopy[self.N + 1 - y][x]]
                new_grid+=[row]


            for x in range(1, self.N + 1):
                for y in range(1, self.N + 1):
                    gridcopy[x][y]=new_grid[x-1][y-1]
            #clear()
            self.show_grid(gridcopy,self.position.x,self.position.y)
            #time.sleep(g)
            listgrids+=gridcopy
            z=z+1

        if gridcopy[self.position.y][self.position.x] == " # ":


            #clear()
            self.show_grid(self.grid,self.position.x,self.position.y)

            print("CANNOT ROTATE CLOCKWISE  TwT \a \a GOING BACK (NOT BACK TO FUTURE) ")
            #time.sleep(g)
            return 0
        else:
            self.grid=gridcopy
            #for x in range(0,len(listgrids)):
             #   self.show_grid(listgrids[x],self.position.x,self.position.y)
            if gridcopy[self.position.y][self.position.x] == " * ":
                return -(self.N//3)*m
            elif gridcopy[self.position.y][self.position.x] == " X ":
                return -(self.N//3)*m
            else:
                return int(gridcopy[self.position.y][self.position.x].strip())*self.N-(self.N//3)*m


    def rotateAnticlockwise(self,m):

        """

        **************************************************MAIN FUNCTION*************************************************
        turns grid anticlockwise by 90 degrees m times
        :param m: no of times grid is to be rotated
        :return: decrease in players energy


        """
        gridcopy=self.grid.copy()
        listgrids = []

        z = 0
        while z < m:
            new_grid = []

            for x in range(1, self.N + 1):
                row = []
                for y in range(1, self.N + 1):
                    row = row + [gridcopy[y][self.N + 1 - x]]
                new_grid += [row]

            for x in range(1, self.N + 1):
                for y in range(1, self.N + 1):
                    gridcopy[x][y] = new_grid[x - 1][y - 1]
            #clear()
            self.show_grid(gridcopy,self.position.x,self.position.y)
            #time.sleep(g)
            listgrids+=gridcopy
            z = z + 1

        if gridcopy[self.position.y][self.position.x] == " # ":
            #clear()
            self.show_grid(self.grid,self.position.x,self.position.y)
            print("CANNOT ROTATE ANTICLOCKWISE TwT \a \a  GOING BACK (NOT BACK TO FUTURE)")
            #time.sleep(g)
            return 0
        else:

            self.grid=gridcopy
            #for x in range(0,len(listgrids)):
             #   self.show_grid(listgrids[x],self.position.x,self.position.y)
            if gridcopy[self.position.y][self.position.x] == " * ":
                return -(self.N//3)*m
            elif gridcopy[self.position.y][self.position.x] == " X ":
                return -(self.N//3)*m
            else:
                return int(gridcopy[self.position.y][self.position.x].strip())*self.N-(self.N//3)*m


class Obstacle(point):

    """


    this class helps in making obstacle
    called by function make_obstacles of class grid to make object of type Obstacle

    derived class of class point


    """
    represent=" # "
    def __init__(self,x,y):
        super().__init__(x,y)


class Reward(point):

    """


    this class helps in making rewards
    called by function make_rewards of class grid to make object of type Obstacle

    derived class of class point


    """
    def __init__(self,x,y):
        super().__init__(x,y)
        self.value=random.randint(1,9)


class Player(point):

    """

    controls energy and move of player according to commands given by player
    derived class of class point


    """
    def __init__(self,x,y,energy):                          #set enery to 2n
        super().__init__(x,y)
        self.energy=energy



    def makeMove(self,s):
        """

        **********************************************MAIN FUNCTION******************************************************
        :param s: input command by user to make player move on grid
        :return: list which is then used to call upgrade_grid of class grid


        """
        #s=s.upper()
        lst=self.find_index(s)
        final=[]
        for x in range(0,len(lst)-1):
            a=s[lst[x]:lst[x+1]]
            final+=[a]
        a=s[lst[-1]:]
        final+=[a]
        return final

    def find_index(self,s):

        """

        HELPER FUNCTION
        finds indices of alphabets in input string by user
        :param s:input string by user
        :return:list of indices of alphabets in input string


        """
        lst=[]
        for x in range(0,len(s)):
            if 65<=ord(s[x])<=90:
                lst+=[int(x)]
        return lst



def clear():
    """
    clears console screen
    :return: None
    """
    if os.name == 'nt':
        _ = os.system('cls')


if __name__=="__main__":
    print("*"*100+"GRID GAME"+"*"*100)
    print("*"*97+"BY:SHUBHAM GARG"+"*"*97)
    print("\n"*2)
    print(" "*93 +"WELCOME DEPRESSED IIITDIAN"+" "*95+"\n"*2)
    n=(input("Nibba, tell me the size of grid,min=5,max=50,default=36   :"))
    if len(n)==0:
        n=0
    else:
        n=int(n)
    if n<5 or n>50:
        n=36
    a=grid(n)
    b=Player(a.start.x,a.start.y,2*n)
    a.show_grid(a.grid,b.x,b.y)
    print("\n"*2)
    print("ENERGY: "+"|"*b.energy+"  ("+str(b.energy)+")\n\n")
    while b.energy>0:
        s=input("SHOW ME YOUR MOVES UWU :")
        s=s.upper()
        ek_list=b.makeMove(s)
        for x in ek_list:
            move=x[0]
            times=int(x[1:])

            if move=="A":
                #print("a me aagya kya? \n\n\n\n")
                clear()                                                             #1
                less_in_energy=a.rotateAnticlockwise(times)
                b.energy += less_in_energy
                if b.energy < 0:
                    print("ENERGY DOWN, GET A REFILL , DRINK RED BULL ,NOOB LMAO ")
                    exit()
                print("ENERGY: " + "|" * b.energy + "  (" + str(b.energy) + ")\n\n")
                time.sleep(g)


            elif move=="C":
                #print("c me aya?\n\n\n")
                clear()                                                              #2
                less_in_energy = a.rotateClockwise(times)
                b.energy += less_in_energy
                if b.energy < 0:
                    print("ENERGY DOWN, GET A REFILL , DRINK RED BULL ,NOOB LMAO ")
                    exit()
                print("ENERGY: " + "|" * b.energy + "  (" + str(b.energy) + ")\n\n")
                time.sleep(g)

            elif move == "U" or "D" or "L" or "R":

                # print("for up down right left \n\n")
                for y in range(0, times):
                    clear()                                                               #3)
                    less_in_energy = a.upgrade_grid(move)
                    b.energy += less_in_energy
                    if b.energy < 0:
                        print("ENERGY DOWN, GET A REFILL , DRINK RED BULL ,NOOB LMAO ")
                        exit()
                    print("ENERGY: " + "|" * b.energy + "  (" + str(b.energy) + ")\n\n")
                    time.sleep(g)





