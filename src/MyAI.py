# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.turning = 0
        self.action_count = 0
        self.xcoord = 0
        self.ycoord = 0
        self.threshold = -300
        self.stuck = 0
        self.checking = 0
        self.tempx = 0
        self.tempy = 0

        self.return_list = []
        self.visited = {}

        self.searching = True
        self.arrow_ready = True
        self.moved_to_next_row = False
        self.wumpus_dead = False
        self.returning = False
        self.turning = False
      
        self.direction = "right"
        self.opposite_direction = "left"
        self.temp_direction = "left"
        pass
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        if(bump):
            self.return_list = self.return_list[1:]
            if(self.direction == "left"):
                self.xcoord += 1
            elif(self.direction == "right"):
                self.xcoord -= 1
            elif(self.direction == "up"):
                self.ycoord -= 1
            elif(self.direction == "down"):
                self.ycoord += 1
        if(bump and (self.xcoord != 0 or self.ycoord != 0)):
            self.stuck += 1
        else:
            self.stuck = 0
        if(scream):
            self.wumpus_dead = True
        if(self.action_count <= self.threshold or self.stuck >= 4):
            self.searching = False
            self.returning = True
        elif(self.xcoord == 0 and self.ycoord == 0 and self.direction == "down" and self.checking == 0):
            self.searching = False
            self.returning = True
        if(self.stuck >= 4 and self.direction == "left"):
            return self.turn_left()
        for key in self.visited.keys():
            if (self.visited[key] >= 4):
                self.searching = False
                self.returning = True

                    
        if(glitter):
            self.searching = False
            self.returning = True
            self.action_count -= 1
            return Agent.Action.GRAB
        if(self.searching):
            if(self.checking == 0 and not breeze and not bump and (not stench or self.wumpus_dead) and 
                (self.direction == "left" or self.direction == "right")):
                if((self.xcoord,self.ycoord) not in self.visited.keys()):
                    self.visited[(self.xcoord,self.ycoord)] = 1
                else:
                    self.visited[(self.xcoord,self.ycoord)] += 1
                if(self.visited[(self.xcoord,self.ycoord)] == 1):
                    self.checking = 7
                    self.temp_direction = self.direction
                    self.tempx = self.xcoord
                    self.tempy = self.ycoord
            if(self.checking != 0):
                return self.check_up_and_down(bump, breeze, stench)

            if(scream and not breeze and (self.direction == "left" or self.direction == "right")):
                self.fill_return_list()
                return self.move_forward()
            if(stench and self.arrow_ready and not self.wumpus_dead and not breeze):
                self.arrow_ready = False
                self.action_count -= 10
                return Agent.Action.SHOOT
            if(((stench and not self.wumpus_dead) or breeze) and self.xcoord == 0 and self.ycoord == 0):
                return Agent.Action.CLIMB

            if(bump and not breeze and (not stench or self.wumpus_dead)):
                if(self.direction == "down" and self.xcoord == 0):
                    return self.turn_left()
                elif(self.direction == "down" and self.xcoord != 0):
                    return self.turn_right()
                self.moved_to_next_row = True
                self.turning = True
                if(self.direction == "left"):
                    return self.turn_right()
                elif(self.direction == "right"):
                    return self.turn_left() 
            if(self.moved_to_next_row and not breeze and (not stench or self.wumpus_dead)):
                if(self.turning):
                    self.turning = False
                    self.fill_return_list()
                    return self.move_forward()
                elif(self.xcoord == 0):
                    self.moved_to_next_row = False
                    return self.turn_right()
                else:
                    self.moved_to_next_row = False
                    return self.turn_left()
            elif(self.moved_to_next_row and (breeze or (stench and not self.wumpus_dead))):
                 self.moved_to_next_row = False
    
            if((breeze or (stench and not self.wumpus_dead)) and not self.turning):
                self.turning = True
                self.turn_around()   
            if(self.turning and (self.direction != self.opposite_direction)):
                return self.turn_left()
            elif(self.turning and (self.direction == self.opposite_direction)):
                self.turning = False
                self.fill_return_list()
                return self.move_forward()
            self.fill_return_list()
            return self.move_forward()

        elif(self.returning):
            if(len(self.return_list) > 2 and self.return_list[0] == "up" and self.return_list[1] == "down"):
                self.return_list = self.return_list[2:]
            elif(len(self.return_list) > 2 and self.return_list[0] == "up" and self.return_list[1] == "up" 
                and self.return_list[2] == "down" and self.return_list[3] == "down"):
                self.return_list = self.return_list[4:]

            if(len(self.return_list) == 0 or (self.xcoord == 0 and self.ycoord == 0)):
                return Agent.Action.CLIMB
            elif(self.direction == "down" and self.ycoord == 0):
                return self.turn_right()
            elif(self.direction == "left" and self.ycoord == 0):
                return self.move_forward()
            elif(self.direction == "down" and self.xcoord == 0):
                return self.move_forward()
            elif(self.direction != self.return_list[0]):
                return self.matching_directions()
            else:
                self.return_list = self.return_list[1:]
                return self.move_forward() 
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
    def check_up_and_down(self, bump, breeze, stench):
        if(self.checking == 7):
            if((self.xcoord,self.ycoord-1) not in self.visited.keys()):
                if(self.direction == "left"):
                    self.checking -= 1
                    return self.turn_right()
                elif(self.direction == "right"):
                    self.checking -= 1
                    return self.turn_left()
            self.checking -= 6

        if(self.checking == 6):
            if(not bump and not breeze and (not stench or self.wumpus_dead)):
                self.fill_return_list()
                return self.move_forward()
            self.checking -= 1

        if(self.checking == 5 or self.checking == 4):
            self.checking -= 1
            return self.turn_right()

        if(self.checking == 3):
            if(self.xcoord != self.tempx or self.ycoord != self.tempy):
                self.fill_return_list()
                return self.move_forward()
            self.checking -= 1
            
        if(self.checking == 2):
            if(self.temp_direction == "left"):
                self.checking -= 1
                return self.turn_right()
            elif(self.temp_direction == "right"):
                self.checking -= 1
                return self.turn_left()

        if(self.checking == 1):
            self.checking -= 1
            self.fill_return_list()
            return self.move_forward()


    def matching_directions(self):
        if(self.direction == "right"):
            if self.return_list[0] == "down":
                return self.turn_right()
            else:
                return self.turn_left()
        elif(self.direction == "up"):
            if self.return_list[0] == "right":
                return self.turn_right()
            else:
                return self.turn_left()
        elif(self.direction == "left"):
            if self.return_list[0] == "down":
                return self.turn_left()
            else:
                return self.turn_right()
        elif(self.direction == "down"):
            if self.return_list[0] == "right":
                return self.turn_left()
            else:
                return self.turn_right()
                
    def move_forward(self):
        self.action_count -= 1
        if(self.direction == "right"):
            self.xcoord += 1
        elif(self.direction == "left"):
            self.xcoord -= 1
        elif(self.direction == "up"):
            self.ycoord += 1
        elif(self.direction == "down"):
            self.ycoord -= 1
        return Agent.Action.FORWARD

    def turn_left(self):
        if self.direction == "right":
            self.direction = "up"
        elif self.direction == "up":
            self.direction = "left"
        elif self.direction == "left":
            self.direction = "down"
        elif self.direction == "down":
            self.direction = "right"
        self.action_count -= 1
        return Agent.Action.TURN_LEFT
 
    def turn_right(self):
        if self.direction == "right":
            self.direction = "down"
        elif self.direction == "down":
            self.direction = "left"
        elif self.direction == "left":
            self.direction = "up"
        elif self.direction == "up":
            self.direction = "right"
        self.action_count -= 1
        return Agent.Action.TURN_RIGHT
   
    def turn_around(self):
        if self.direction == "right":
            self.opposite_direction = "left"
        elif self.direction == "left":
            self.opposite_direction = "right"
        elif self.direction == "up":
            self.opposite_direction = "down"
        elif self.direction == "down":
            self.opposite_direction = "up"

    def fill_return_list(self):
        if self.direction == "right":
            self.return_list.insert(0,"left")
        elif self.direction == "left":
            self.return_list.insert(0,"right")
        elif self.direction == "up":
            self.return_list.insert(0,"down")
        elif self.direction == "down":
            self.return_list.insert(0,"up")
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
