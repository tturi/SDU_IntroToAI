import time
start_time = time.time()

class Map:
    Walls = [
    [True, True, True, True, True, True, True, True, True, True, True, True],
    [True, True, False, False, False, True, False, False, False, False, False, True],
    [True, True, False, False, False, True, False, False, False, False, False, True],
    [True, True, False, False, False, False, True, False, False, True, True, True],
    [True, False, False, False, False, False, False, False, True, True, True, True],
    [True, False, False, False, True, False, False, False, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True, True, True]
    ]
    Goals = [
    [False, False, False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, True, True, False, False, False],
    [False, False, False, False, False, False, False, True, True, False, False, False],
    [False, False, False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False, False, False]
    ]
    Weigth = [
    [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
    [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
    [1000, 1000, 1000, 1000, 1000, 1000, 1000, 0, 0, 1000, 1000, 1000],
    [1000, 1000, 1, 1, 1, 1000, 1000, 0, 0, 1000, 1000, 1000],
    [1000, 1000, 1, 1, 1, 1, 1, 1, 1000, 1000, 1000, 1000],
    [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
    [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
    ]

class Step:

    def __init__(self, robot_x, robot_y, explored_route, explored, weigth, box1_x = None, box1_y = None, box2_x = None, box2_y = None, box3_x = None, box3_y = None, box4_x = None, box4_y = None, box5_x = None, box5_y = None):
        self.x = robot_x
        self.y = robot_y
        self.explored_route = str(explored_route)
        self.explored = explored
        self.weigth = weigth
        self.box1_x = box1_x
        self.box1_y = box1_y
        self.box2_x = box2_x
        self.box2_y = box2_y
        self.box3_x = box3_x
        self.box3_y = box3_y
        self.box4_x = box4_x
        self.box4_y = box4_y
        self.box5_x = box5_x
        self.box5_y = box5_y

    def __lt__(self, other):
        return self.weigth < other.weigth

# This list contains the sequance of exploring nodes, also identifies direction. Capital letter denoting movement without box, small letter denoting movement with box
nodeExploring = ["D","U","R","L","d","u","r","l"]

# This variable storing the steps
steps = []

# This is the list of visited nodes/states, which makes no sense to visit again.
visitedStates = {}

# We can check performance by counting visited nodes
examined_node_counter = 0

# We can check performance by counting explored nodes
explored_node_counter = 0

# First step, where the robot start
steps.append(Step(4, 7,"" ,False, 0, 3, 2, 3, 3, 3, 4, 4, 2))

# We will store solution in this variable
Solution = None

# This function is checking if it is a valid step while we do not bring the box with us
def IsValidStepWithoutMovingBox(x, y):
    if Map.Walls[x][y]:
        return False
    return True

# We need must not have a box where want to step and where we are stepping from, because we do not want to turn between two boxes
def DoWeAlreadyHaveaBoxWhereWeWanttoStepandWhereAreSteppingFrom(x1, y1, x2, y2, box1_x, box1_y, box2_x, box2_y, box3_x, box3_y, box4_x, box4_y, box5_x, box5_y):
    x1y1 = str(x1) + str(y1)
    x2y2 = str(x2) + str(y2)
    boxStatus = []
    box1_xbox1_y = str(box1_x) + str(box1_y)
    boxStatus.append(box1_xbox1_y)
    box2_xbox2_y = str(box2_x) + str(box2_y)
    boxStatus.append(box2_xbox2_y)
    box3_xbox3_y = str(box3_x) + str(box3_y)
    boxStatus.append(box3_xbox3_y)
    box4_xbox4_y = str(box4_x) + str(box4_y)
    boxStatus.append(box4_xbox4_y)
    box5_xbox5_y = str(box5_x) + str(box5_y)
    boxStatus.append(box5_xbox5_y)
    if (x1y1 in boxStatus) == True and (x2y2 in boxStatus) == True:
        return True
    return False

# This function is checking if it is a valid step while we bring the box with us. It checks if there is a wall where we want to step, and if we have a box to move on the firstNode field. It doesn not check however if the target step has a box already, therefore I made a new function "DoWeAlreadyHaveaBoxWhereWeWanttoStep"
def IsValidStepWithMovingBox(x1, y1, x2, y2, box1_x, box1_y, box2_x, box2_y, box3_x, box3_y, box4_x, box4_y, box5_x, box5_y):
    xy = str(x1) + str(y1)
    boxStatus = []
    box1_xbox1_y = str(box1_x) + str(box1_y)
    boxStatus.append(box1_xbox1_y)
    box2_xbox2_y = str(box2_x) + str(box2_y)
    boxStatus.append(box2_xbox2_y)
    box3_xbox3_y = str(box3_x) + str(box3_y)
    boxStatus.append(box3_xbox3_y)
    box4_xbox4_y = str(box4_x) + str(box4_y)
    boxStatus.append(box4_xbox4_y)
    box5_xbox5_y = str(box5_x) + str(box5_y)
    boxStatus.append(box5_xbox5_y)
    if Map.Walls[x2][y2]:
        return False
    if (xy in boxStatus) != True:
        return False
    return True

# We need must not have a box where want to step with a box, since we cannot have 2 boxes at one place
def DoWeAlreadyHaveaBoxWhereWeWanttoStep(x, y, box1_x, box1_y, box2_x, box2_y, box3_x, box3_y, box4_x, box4_y, box5_x, box5_y):
    xy = str(x) + str(y)
    boxStatus = []
    box1_xbox1_y = str(box1_x) + str(box1_y)
    boxStatus.append(box1_xbox1_y)
    box2_xbox2_y = str(box2_x) + str(box2_y)
    boxStatus.append(box2_xbox2_y)
    box3_xbox3_y = str(box3_x) + str(box3_y)
    boxStatus.append(box3_xbox3_y)
    box4_xbox4_y = str(box4_x) + str(box4_y)
    boxStatus.append(box4_xbox4_y)
    box5_xbox5_y = str(box5_x) + str(box5_y)
    boxStatus.append(box5_xbox5_y)
    if (xy in boxStatus) == True:
        return True
    return False

# This function is checking if we have visited the node before.
def IsVisitedBefore(x, y, box1_x, box1_y, box2_x, box2_y, box3_x, box3_y, box4_x, box4_y, box5_x, box5_y):
    global visitedStates
    stateCode = str(x) + str(y) + str(box1_x) + str(box1_y) + str(box2_x) + str(box2_y) + str(box3_x) + str(box3_y) + str(box4_x) + str(box4_y) + str(box5_x) + str(box5_y)
    if stateCode in visitedStates:
        return True
    return False

# This function is checking if the current state is a solution. It helps breaking the loop when we got an optimal solution, the number of boxes has to be adjusted! # and Map.Goals[Node.box2_x][Node.box2_y] and Map.Goals[Node.box3_x][Node.box3_y] and Map.Goals[Node.box4_x][Node.box4_y] and Map.Goals[Node.box5_x][Node.box5_y]) == True:
def IsSolution(Firstnode):
    if (Map.Goals[Firstnode.box1_x][Firstnode.box1_y] and Map.Goals[Firstnode.box2_x][Firstnode.box2_y] and Map.Goals[Firstnode.box3_x][Firstnode.box3_y] and Map.Goals[Firstnode.box4_x][Firstnode.box4_y]) == True:
        return True
    return False

# This function define which box will move in case of a step where we want to move a box
def UpdateBoxStateWhichIsMoving(BoxMovingStep, FirstNode):
    i = BoxMovingStep.x - FirstNode.x
    j = BoxMovingStep.y - FirstNode.y
    xy = str(FirstNode.x) + str(FirstNode.y)
    box1_xbox1_y = str(FirstNode.box1_x) + str(FirstNode.box1_y)
    box2_xbox2_y = str(FirstNode.box2_x) + str(FirstNode.box2_y)
    box3_xbox3_y = str(FirstNode.box3_x) + str(FirstNode.box3_y)
    box4_xbox4_y = str(FirstNode.box4_x) + str(FirstNode.box4_y)
    box5_xbox5_y = str(FirstNode.box5_x) + str(FirstNode.box5_y)
    if box1_xbox1_y == xy:
        BoxMovingStep.box1_x = BoxMovingStep.box1_x + i
        BoxMovingStep.box1_y = BoxMovingStep.box1_y + j
    elif box2_xbox2_y == xy:
        BoxMovingStep.box2_x = BoxMovingStep.box2_x + i
        BoxMovingStep.box2_y = BoxMovingStep.box2_y + j
    elif box3_xbox3_y == xy:
        BoxMovingStep.box3_x = BoxMovingStep.box3_x + i
        BoxMovingStep.box3_y = BoxMovingStep.box3_y + j
    elif box4_xbox4_y == xy:
        BoxMovingStep.box4_x = BoxMovingStep.box4_x + i
        BoxMovingStep.box4_y = BoxMovingStep.box4_y + j
    elif box5_xbox5_y == xy:
        BoxMovingStep.box5_x = BoxMovingStep.box5_x + i
        BoxMovingStep.box5_y = BoxMovingStep.box5_y + j

# This function explore unexplored node and create new ones. At the end, it removed the explored node from the steps list, this way saving memory.
def exploreNewNodesOnLevel(steps):
    global examined_node_counter
    global explored_node_counter
    global Solution
    global visitedStates
    FirstNode = steps[0]
    if IsSolution(FirstNode) == True:
        Solution = FirstNode.explored_route
        return Solution
    i = 0
    stateCode = str(FirstNode.x) + str(FirstNode.y) + str(FirstNode.box1_x) + str(FirstNode.box1_y) + str(FirstNode.box2_x) + str(FirstNode.box2_y) + str(FirstNode.box3_x) + str(FirstNode.box3_y) + str(FirstNode.box4_x) + str(FirstNode.box4_y) + str(FirstNode.box5_x) + str(FirstNode.box5_y)
    visitedStates[stateCode] = "True"
    explored_node_counter += 1
    for direction in nodeExploring:
        examined_node_counter += 1
        if (direction == "D" and IsValidStepWithoutMovingBox(FirstNode.x+1, FirstNode.y) and IsVisitedBefore(FirstNode.x+1, FirstNode.y, FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y) != True and DoWeAlreadyHaveaBoxWhereWeWanttoStepandWhereAreSteppingFrom(FirstNode.x, FirstNode.y, FirstNode.x+1, FirstNode.y, FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y) == False):
            steps.append(Step(FirstNode.x+1, FirstNode.y, str(FirstNode.explored_route + "D"), False, int(FirstNode.weigth + Map.Weigth[FirstNode.x+1][FirstNode.y]), FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y))
            i += 1
        if (direction == "U" and IsValidStepWithoutMovingBox(FirstNode.x-1, FirstNode.y) and IsVisitedBefore(FirstNode.x-1, FirstNode.y, FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y) != True and DoWeAlreadyHaveaBoxWhereWeWanttoStepandWhereAreSteppingFrom(FirstNode.x, FirstNode.y, FirstNode.x-1, FirstNode.y, FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y) == False):
            steps.append(Step(FirstNode.x-1, FirstNode.y, str(FirstNode.explored_route + "U"), False, int(FirstNode.weigth + Map.Weigth[FirstNode.x-1][FirstNode.y]), FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y))
            i += 1
        if (direction == "R" and IsValidStepWithoutMovingBox(FirstNode.x, FirstNode.y+1) and IsVisitedBefore(FirstNode.x, FirstNode.y+1, FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y) != True and DoWeAlreadyHaveaBoxWhereWeWanttoStepandWhereAreSteppingFrom(FirstNode.x, FirstNode.y, FirstNode.x, FirstNode.y+1, FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y) == False):
            steps.append(Step(FirstNode.x, FirstNode.y+1, str(FirstNode.explored_route + "R"), False, int(FirstNode.weigth + Map.Weigth[FirstNode.x][FirstNode.y+1]), FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y))
            i += 1
        if (direction == "L" and IsValidStepWithoutMovingBox(FirstNode.x, FirstNode.y-1) and IsVisitedBefore(FirstNode.x, FirstNode.y-1, FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y) != True and DoWeAlreadyHaveaBoxWhereWeWanttoStepandWhereAreSteppingFrom(FirstNode.x, FirstNode.y, FirstNode.x, FirstNode.y-1, FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y) == False):
            steps.append(Step(FirstNode.x, FirstNode.y-1, str(FirstNode.explored_route + "L"), False, int(FirstNode.weigth + Map.Weigth[FirstNode.x][FirstNode.y-1]), FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y))
            i += 1
        if (direction == "d" and IsValidStepWithMovingBox(FirstNode.x, FirstNode.y, FirstNode.x + 1, FirstNode.y, FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y) and DoWeAlreadyHaveaBoxWhereWeWanttoStep(FirstNode.x+1, FirstNode.y, FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y) == False):
            steps.append(Step(FirstNode.x+1, FirstNode.y, str(FirstNode.explored_route + "d"), False, int(FirstNode.weigth + Map.Weigth[FirstNode.x+1][FirstNode.y]), FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y))
            i += 1
            UpdateBoxStateWhichIsMoving(steps[len(steps)-1],FirstNode)
            if (IsVisitedBefore(steps[len(steps)-1].x, steps[len(steps)-1].y, steps[len(steps)-1].box1_x, steps[len(steps)-1].box1_y, steps[len(steps)-1].box2_x, steps[len(steps)-1].box2_y, steps[len(steps)-1].box3_x, steps[len(steps)-1].box3_y, steps[len(steps)-1].box4_x, steps[len(steps)-1].box4_y, steps[len(steps)-1].box5_x, steps[len(steps)-1].box5_y)) == True:
                steps.pop()
                i -= 1
        if (direction == "u" and IsValidStepWithMovingBox(FirstNode.x, FirstNode.y, FirstNode.x - 1, FirstNode.y, FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y) and DoWeAlreadyHaveaBoxWhereWeWanttoStep(FirstNode.x-1, FirstNode.y, FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y) == False):
            steps.append(Step(FirstNode.x-1, FirstNode.y, str(FirstNode.explored_route + "u"), False, int(FirstNode.weigth + Map.Weigth[FirstNode.x-1][FirstNode.y]), FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y))
            i += 1
            UpdateBoxStateWhichIsMoving(steps[len(steps)-1],FirstNode)
            if (IsVisitedBefore(steps[len(steps)-1].x, steps[len(steps)-1].y, steps[len(steps)-1].box1_x, steps[len(steps)-1].box1_y, steps[len(steps)-1].box2_x, steps[len(steps)-1].box2_y, steps[len(steps)-1].box3_x, steps[len(steps)-1].box3_y, steps[len(steps)-1].box4_x, steps[len(steps)-1].box4_y, steps[len(steps)-1].box5_x, steps[len(steps)-1].box5_y)) == True:
                steps.pop()
                i -= 1
        if (direction == "r" and IsValidStepWithMovingBox(FirstNode.x, FirstNode.y, FirstNode.x, FirstNode.y+1, FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y) and DoWeAlreadyHaveaBoxWhereWeWanttoStep(FirstNode.x, FirstNode.y+1, FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y) == False):
            steps.append(Step(FirstNode.x, FirstNode.y+1, str(FirstNode.explored_route + "r"), False, int(FirstNode.weigth + Map.Weigth[FirstNode.x][FirstNode.y+1]), FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y))
            i += 1
            UpdateBoxStateWhichIsMoving(steps[len(steps)-1],FirstNode)
            if (IsVisitedBefore(steps[len(steps)-1].x, steps[len(steps)-1].y, steps[len(steps)-1].box1_x, steps[len(steps)-1].box1_y, steps[len(steps)-1].box2_x, steps[len(steps)-1].box2_y, steps[len(steps)-1].box3_x, steps[len(steps)-1].box3_y, steps[len(steps)-1].box4_x, steps[len(steps)-1].box4_y, steps[len(steps)-1].box5_x, steps[len(steps)-1].box5_y)) == True:
                steps.pop()
                i -= 1
        if (direction == "l" and IsValidStepWithMovingBox(FirstNode.x, FirstNode.y, FirstNode.x, FirstNode.y - 1, FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y) and DoWeAlreadyHaveaBoxWhereWeWanttoStep(FirstNode.x, FirstNode.y-1, FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y) == False):
            steps.append(Step(FirstNode.x, FirstNode.y-1, str(FirstNode.explored_route + "l"), False, int(FirstNode.weigth + Map.Weigth[FirstNode.x][FirstNode.y-1]), FirstNode.box1_x, FirstNode.box1_y, FirstNode.box2_x, FirstNode.box2_y, FirstNode.box3_x, FirstNode.box3_y, FirstNode.box4_x, FirstNode.box4_y, FirstNode.box5_x, FirstNode.box5_y))
            i += 1
            UpdateBoxStateWhichIsMoving(steps[len(steps)-1],FirstNode)
            if (IsVisitedBefore(steps[len(steps)-1].x, steps[len(steps)-1].y, steps[len(steps)-1].box1_x, steps[len(steps)-1].box1_y, steps[len(steps)-1].box2_x, steps[len(steps)-1].box2_y, steps[len(steps)-1].box3_x, steps[len(steps)-1].box3_y, steps[len(steps)-1].box4_x, steps[len(steps)-1].box4_y, steps[len(steps)-1].box5_x, steps[len(steps)-1].box5_y)) == True:
                steps.pop()
                i -= 1
    FirstNode.explored = True
    del steps[0]

def Solve(steps):
    while Solution == None and len(steps) != 0:
        exploreNewNodesOnLevel(steps)
        steps.sort()
    if Solution != None:
        print("The program visited", examined_node_counter, "nodes during the whole execution, and explored", explored_node_counter, "nodes.")
        print("The last FIFO explored contains", len(steps), "unexplored nodes when the process terminated with solution.")
        print("The solution is:", Solution)
        print("The program executed in", time.time() - start_time, "[second].")
        print("The visited states list length is:", len(visitedStates))
    else:
        print("The program visited", examined_node_counter, "nodes during the whole execution.")
        print("There is no solution found.")
        print("The program executed in", time.time() - start_time, "[second].")
        print("The visited states list length is:", len(visitedStates))

Solve(steps)

input("Press ENTER to exit")