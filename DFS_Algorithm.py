# This program uses a library to generate the maze, the library is called pyamaze
# You can install this library using pip by 'pip install pyamaze' or you can run 'pip install -r requirements' in this directory
from pyamaze import maze, COLOR, agent

# You'll need to change this to the path where it contains the maze_config.txt file
path_to_config = "maze_config.txt"

# This function read text from the "maze_config.txt" file and extract corresponding variables to form the maze
def extract_variables(file_name):
    with open(file_name, "r") as file:
        contents = file.read()
        
        number_of_rows_index = contents.index("number of rows =") + len("number of rows =")
        number_of_rows_end_index = contents.index("\n", number_of_rows_index)
        number_of_rows = int(contents[number_of_rows_index:number_of_rows_end_index])
        
        number_of_columns_index = contents.index("number of columns =") + len("number of columns =")
        number_of_columns_end_index = contents.index("\n", number_of_columns_index)
        number_of_columns = int(contents[number_of_columns_index:number_of_columns_end_index])
        
        start_location_index = contents.index("start_location = (") + len("start_location = (")
        start_location_end_index = contents.index(")", start_location_index)
        start_location_values = contents[start_location_index:start_location_end_index].split(",")
        start_location = (int(start_location_values[0]), int(start_location_values[1]))
        
        end_location_index = contents.index("end_location = (") + len("end_location = (")
        end_location_end_index = contents.index(")", end_location_index)
        end_location_values = contents[end_location_index:end_location_end_index].split(",")
        end_location = (int(end_location_values[0]), int(end_location_values[1]))
        
    return {"number_of_rows": number_of_rows, "number_of_columns": number_of_columns, "start_location": start_location, "end_location": end_location}

# The function take in a string parameter represents the path to the maze_config.txt file
maze_config = extract_variables(path_to_config)

# Extract variables including rows, columns to form the size of the maze, then start location and end location inside the maze
maze_rows = maze_config["number_of_rows"]
maze_columns = maze_config["number_of_columns"]

start_loc = maze_config["start_location"]
end_loc = maze_config["end_location"]

# This function is the DFS (Depth First Search) algorithm, but it includes every path that the algorithm has travelled in the maze to later visualize how the algorithm works in the maze
def all_paths(maze):
    # Initialize neccessary variables
    current_loc = start_loc

    intersected = list()
    explored = list()
    temp_path = list()

    dfs_path = [start_loc]

    solved_path = dict()

    # Keep finding paths until it reach the end point
    while current_loc != end_loc:

        # When starting in a new location, the direction will first set to be 0 
        direction = 0
        # Add the current location to explored list, means the DFS has travelled to this location
        explored.append(current_loc)
        # Go through every direction at the current location, if there exists a way, direction will add 1, otherwise it remains unchange, also add the new location to intersected list, which is like a stack in DFS to store back up locations, these locations will open new directions and they will be explored later.
        if maze.maze_map[(current_loc)]['E']:
            direction += 1
            new_loc = (current_loc[0], current_loc[1]+1)
            intersected.append(new_loc)

        if maze.maze_map[(current_loc)]['W']:
            direction += 1
            new_loc = (current_loc[0], current_loc[1]-1)
            intersected.append(new_loc)

        if maze.maze_map[(current_loc)]['N']:
            direction += 1
            new_loc = (current_loc[0]-1, current_loc[1])
            intersected.append(new_loc)

        if maze.maze_map[(current_loc)]['S']:
            direction += 1
            new_loc = (current_loc[0]+1, current_loc[1])
            intersected.append(new_loc)

        # Direction == 1 means that it has reached the dead-end in the current path, this path will be added to the dfs_path because the purpose of this function is to demonstrate how the algorithm travelled/performed
        if direction == 1:
            dfs_path.extend(temp_path)
            temp_path.clear()
        
        # If there are common directions/locations in between intersected list and explored list, it will be removed to prevent travelling back to where it has been through/explored before
        common_elements = set(intersected).intersection(set(explored))
        if common_elements: 
            intersected.remove(common_elements.pop())

        # If the stack/interseted list only has 1 location, that means the DFS is travelling in a 1-way path, there is no intersect so this location will be added straight to the dfs_path
        if len(intersected) == 1:
            current_loc = intersected.pop()
            dfs_path.append(current_loc)

        # If there are any intersect paths, the temp_path will explore all of those paths all the way to the dead-end and add all the paths to dfs_path
        elif len(intersected) > 1:
            current_loc = intersected.pop()
            temp_path.append(current_loc)

        # If current location is end location, means the algorithm has reached the destination, add the current temp path to dfs_path
        if current_loc == end_loc:
            dfs_path.extend(temp_path)

    # Add the last location to the explored list (this is not neccessary at all)
    explored.append(end_loc)

    # Convert the path to dictionary format and return
    for i in range(len(dfs_path)-1):
        solved_path[dfs_path[i]] = dfs_path[i+1]

    return solved_path


# This function is also the DFS (Depth First Search) algorithm, but it only includes the main path that the algorithm has travelled in the maze to the end point and it will later be visualized after the above DFS has demonstrated how has it found every paths
def main_path(maze):
    # Initialize neccessary variables
    current_loc = start_loc

    stack = [current_loc]
    explored = set()
    traveled_path = dict()

    while stack:
        current_loc = stack.pop()
        explored.add(current_loc)

        # Keep finding paths until it reach the end point
        if current_loc == end_loc:
            break
        
        # Search for all available directions of the current position
        for direction in maze.maze_map[current_loc]:
            # Loop through every direction and assign them to new_loc
            if maze.maze_map[current_loc][direction]:

                if direction == 'E':
                    new_loc = (current_loc[0], current_loc[1]+1)

                elif direction == 'W':
                    new_loc = (current_loc[0], current_loc[1]-1)

                elif direction == 'N':
                    new_loc = (current_loc[0]-1, current_loc[1])

                elif direction == 'S':
                    new_loc = (current_loc[0]+1, current_loc[1])

                # If this location is new/hasn't been in explored set, it will be added to stack and assgined as key for values which is the previous location
                if new_loc not in explored:
                    stack.append(new_loc)
                    traveled_path[new_loc] = current_loc

    main_path = dict()
    loc = end_loc
    # Reverse the dictionary to find the main path from the start to the end and return it
    while loc != start_loc:
        main_path[traveled_path[loc]] = loc
        loc = traveled_path[loc]

    return main_path

if __name__=='__main__':
    # Initialize the maze and its size
    m=maze(rows=maze_rows, cols=maze_columns)
    # Show the end location in the maze
    m.CreateMaze(end_loc[0], end_loc[1])
    all_dfs_path=all_paths(m)
    # Initialize an agent to visualize the all_paths function above, which will display every paths that the DFS has travelled (this path will be in blue color)
    a1=agent(m,footprints=True,filled=True,color=COLOR.blue)
    a1.position=start_loc
    main_dfs_path=main_path(m)
    # Initialize another agent to visualize the main_path function above, which will display only the main path from the start to the end (this path will be in red color)
    a2=agent(m,footprints=True,filled=True,color=COLOR.red)
    a2.position=start_loc
    # This is not necessary at all too, but the library by default create a starting point at the bottom right corner of the maze and they will inherits configuration of the last agent, so this agent was create to cover that part.
    a=agent(m,footprints=False,filled=True,color=COLOR.dark)
    # Trace the paths that the agents has travelled
    m.tracePath({a1:all_dfs_path})
    m.tracePath({a2:main_dfs_path})
    m.run()
            
