from Queue import PriorityQueue

def General_Search(connection_dict, search_method, heuristic_dict):
    queue = [['S']]  # problem.initalState
    safety_count = 0
    local_flag = True #for IDS
    l_state_change = False
    depth_limit = 2
    if search_method == "IDS":
        print "L = 0"
    print "Expanded = ", queue[0][0]
    if search_method in ["UCS","GS", "A*"]:
        print "Queue =  [<0.0"+ str(queue[0]) +">]"
    else:
        print "Queue =", queue
    if search_method == "IDS":
        print "\n"
    idl_depth_limit = 1

    while (len(queue) != 0 and safety_count < 25):
        if queue == None:
            return ["No path found!"]
        leftmost_of_queue = queue[0][0]
        if leftmost_of_queue == 'G':
            print "Goal Found! \n"
            return queue
        popped = queue.pop(0)
        key_to_expand = popped[0]

        if search_method == "DFS":
            opened_nodes = sorted(connection_dict[key_to_expand], reverse = True)
            for l in opened_nodes:
                if l != 'S' and l not in popped:
                    items_to_insert = [l] + popped
                    queue.insert(0, items_to_insert)

        elif search_method == "BFS":
            opened_nodes = sorted(connection_dict[key_to_expand])
            for l in opened_nodes:
                if l != 'S' and l not in popped:
                    items_to_insert = [l] + popped
                    queue.append(items_to_insert)

        elif search_method == "DLS":
            if len(popped) < depth_limit + 1:
                opened_nodes = sorted(connection_dict[key_to_expand], reverse = True)
                # print  "Opened Nodes = ", opened_nodes
                # print popped
                for l in opened_nodes:
                    # print "expanded elements = ", l
                    # print "l", l, " not in popped", popped, ":", l not in popped
                    if l != 'S' and l not in popped:
                        items_to_insert = [l] + popped
                        queue.insert(0, items_to_insert)

            else:
                # print "Nulling popped!"
                # popped = []
                pass

        elif search_method == "IDS":
            if idl_depth_limit == 1 and local_flag:
                print "L =", idl_depth_limit
                print "Expanded = ", popped[0]
                print "Queue = ", [popped]
                local_flag = False

            if len(popped) < idl_depth_limit + 1 and 'G' not in popped:
                opened_nodes = sorted(connection_dict[key_to_expand], reverse = True)
                for l in opened_nodes:
                    if l != 'S' and l not in popped:
                        items_to_insert = [l] + popped
                        # print "Items to insert =", items_to_insert
                        queue.insert(0, items_to_insert)
                        # print "Q after insert ", queue

            elif "G" not in popped:
                idl_depth_limit +=1
                l_state_change = True

        elif search_method == "UCS":
            opened_nodes = sorted(connection_dict[key_to_expand])
            items_to_insert = []
            for node in opened_nodes:
                if node in popped:
                    continue
                items_to_insert.append([node] + popped)
            queue.extend(items_to_insert)

            def comparator(list1, list2):
                if cost_of_path(list1, connection_dict) > cost_of_path(list2, connection_dict):
                    return 1
                elif cost_of_path(list1, connection_dict) < cost_of_path(list2, connection_dict):
                    return -1
                else:
                    if list1[0] > list2[0]:
                        return 1
                    return -1
            queue.sort(comparator)

        elif search_method == "GS":
            opened_nodes = sorted(connection_dict[key_to_expand])
            items_to_insert = []
            for node in opened_nodes:
                if node in popped:
                    continue
                items_to_insert.append([node]+popped)
            queue.extend(items_to_insert)

            def h_comparator(list1, list2):
                if float(heuristic_dict[list1[0]]) > float(heuristic_dict[list2[0]]):
                    return 1
                elif float(heuristic_dict[list1[0]]) < float(heuristic_dict[list2[0]]):
                    return -1
                else:
                    if list1[0] == list2[0]:
                        if len(list1)>len(list2):
                            return 1
                        else:
                            return -1

                    elif list1[0] > list2[0]:
                        return 1
                    return -1
            queue.sort(h_comparator)

        elif search_method == "A*":
            opened_nodes = sorted(connection_dict[key_to_expand])
            items_to_insert = []
            for node in opened_nodes:
                if node in popped:
                    continue
                items_to_insert.append([node] + popped)
            queue.extend(items_to_insert)

            def astar_comparator(list1, list2):
                if cost_of_path(list1, connection_dict) + float(heuristic_dict[list1[0]]) > cost_of_path(list2, connection_dict) + float(heuristic_dict[list2[0]]):
                    return 1
                elif cost_of_path(list1, connection_dict) + float(heuristic_dict[list1[0]]) < cost_of_path(list2, connection_dict) + + float(heuristic_dict[list2[0]]):
                    return -1
                else:
                    if list1[0] == list2[0]:
                        if len(list1)>len(list2):
                            return 1
                        else:
                            return -1

                    elif list1[0] > list2[0]:
                        return 1
                    return -1
            queue.sort(astar_comparator)
            queue = remove_duplicates(queue)

        elif search_method == "HCS": #Hill climbing search
            opened_nodes = sorted(connection_dict[key_to_expand])
            items_to_insert = []

            for node in opened_nodes:
                if node in popped:
                    continue
                items_to_insert.append([node] + popped)


            def hc_comparator(list1, list2):
                if float(heuristic_dict[list1[0]]) > float(heuristic_dict[list2[0]]):
                    return 1
                elif float(heuristic_dict[list1[0]]) < float(heuristic_dict[list2[0]]):
                    return -1
                else:
                    if list1[0] == list2[0]:
                        if len(list1)>len(list2):
                            return 1
                        else:
                            return -1

                    elif list1[0] > list2[0]:
                        return 1
                    return -1

            items_to_insert.sort(hc_comparator)

            queue.insert(0, items_to_insert[0])
        
        if l_state_change:
            queue = [['S']]
        print_queue_state(queue, connection_dict, search_method, l_state_change, idl_depth_limit, heuristic_dict=heuristic_dict)
        if l_state_change:
            l_state_change = False
        safety_count += 1

def remove_duplicates(q):
    list_of_duplicate_index = []
    for index in range(len(q)):
        search = q[index][0]
        #         print search
        for j in range(index + 1, len(q)):
            if q[j][0] == search:
                #                 print "Got 'em!!", search, "at", q[j], j
                list_of_duplicate_index.append(j)
                #                 print list_of_duplicate_index
                break
    for i in list_of_duplicate_index:
        del q[i]
    return q

def cost_of_path(path, connection_dict):
    if len(path) in [0, 1]:
        return 0
    cost = 0.0
    for idx in range(0, len(path) - 1):
        cost += float(connection_dict[path[idx]][path[idx + 1]])
    return cost
def heuristic_cost_of_path(path, heuristic_dict):
    # print type(heuristic_dict[path[0]])
    return float(heuristic_dict[path[0]])
# To print the queue according to the specific search algorithm
def print_queue_state(queue, connection_dict, search_method, l_state_change, idl_depth_limit, heuristic_dict):
    if search_method in ["DFS", "BFS", "DLS", "IDS", "HCS"]:
        if search_method == "IDS":
            if l_state_change:
                print "\n"
                print "L =", idl_depth_limit

        if len(queue) != 0:
            print "Expanded = ", queue[0][0]
            print "Queue = ", queue
    elif search_method in ["UCS", "GS", "A*"]:
        if len(queue) != 0:
            print "Expanded =", queue[0][0]

            if search_method == "UCS":
                string_print = ''
                for idx in range(len(queue)):
                    current_path = queue[idx]
                    current_cost_of_path = cost_of_path(current_path, connection_dict)
                    string_print = string_print + '<' + str(current_cost_of_path) + '' + str(current_path) + '>, '

                print '[' + string_print[:-2] + ']'

            elif search_method == "GS":
                string_print = ''
                for idx in range(len(queue)):
                    current_path = queue[idx]
                    # current_cost_of_path = heuristic_dict[current_path[0]]
                    current_cost_of_path = heuristic_cost_of_path(current_path, heuristic_dict)
                    string_print = string_print + '<' + str(current_cost_of_path) + '' + str(current_path) + '>, '

                print '[' + string_print[:-2] + ']'

            elif search_method == "A*":
                string_print = ''
                for idx in range(len(queue)):
                    current_path = queue[idx]
                    current_cost_of_path = cost_of_path(current_path, connection_dict) + heuristic_cost_of_path(current_path, heuristic_dict)
                    string_print = string_print + '<' + str(current_cost_of_path) + '' + str(current_path) + '>, '

                print '[' + string_print[:-2] + ']'





