BOARD_SIZE = 9 # or any number that have Square roots like 16, 25, 36
SQUARE_SIZE = int(BOARD_SIZE**.5)

def check_possibilities(page):
    possibilities = []
    for i in range(BOARD_SIZE):
        possibilities.append([])
        for j in range (BOARD_SIZE):
            possibilities[i].append(list(range(1, BOARD_SIZE+1)))

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if page[row][col] != 0:
                possibilities[row][col] = []
                for i in range(BOARD_SIZE):
                    if page[row][col] in possibilities[row][i]:
                        possibilities[row][i].remove(page[row][col])
                    if page[row][col] in possibilities[i][col]:
                        possibilities[i][col].remove(page[row][col])
                
                for i in range(SQUARE_SIZE):
                    for j in range(SQUARE_SIZE):
                        if SQUARE_SIZE*i<=row<SQUARE_SIZE*i+SQUARE_SIZE and SQUARE_SIZE*j<=col<SQUARE_SIZE*j+SQUARE_SIZE:
                            for k in range(SQUARE_SIZE):
                                for l in range(SQUARE_SIZE):
                                    if page[row][col] in possibilities[i*SQUARE_SIZE+k][j*SQUARE_SIZE+l]:
                                        possibilities[i*SQUARE_SIZE+k][j*SQUARE_SIZE+l].remove(page[row][col])

    return possibilities

def check_conflict(page):
    conflict = False
    
    # Row Checking
    for row in range(BOARD_SIZE):
        visited = []
        for col in range(BOARD_SIZE):
            if page[row][col] != 0:
                if page[row][col] not in visited:
                    visited.append(page[row][col])
                else:
                    conflict = True
                    break
        if conflict:
            break
    if conflict:
        return conflict
    # column Checking
    for col in range(BOARD_SIZE):
        visited = []
        for row in range(BOARD_SIZE):
            if page[row][col] != 0:
                if page[row][col] not in visited:
                    visited.append(page[row][col])
                else:
                    conflict = True
                    break
        if conflict:
            break

    if conflict:
        return conflict
    # Box Checking
    for i in range(SQUARE_SIZE):
        for j in range(SQUARE_SIZE):
            visited = []
            for row in range(SQUARE_SIZE):
                for col in range(SQUARE_SIZE):
                    if page[i*SQUARE_SIZE+row][j*SQUARE_SIZE+col] != 0:
                        if page[i*SQUARE_SIZE+row][j*SQUARE_SIZE+col] not in visited:
                            visited.append(page[i*SQUARE_SIZE+row][j*SQUARE_SIZE+col])
                        else:
                            conflict = True
                            break
                if conflict:
                    break
            if conflict:
                break
        if conflict:
            break

    return conflict

def statics_methods (page):
    possibilities = check_possibilities(page)
    page_changed = False

    # Row Check
    for row in range(BOARD_SIZE):
        row_candidate={}
        for i in range(BOARD_SIZE):
            row_candidate[i+1] = 0
        for col in range(BOARD_SIZE):
            for possibility in possibilities[row][col]:
                row_candidate[possibility] += 1
            
        for num in row_candidate:
            if row_candidate[num] == 1:
                for col in range(BOARD_SIZE):
                    for possibility in possibilities[row][col]:
                        if possibility == num:
                            page[row][col] = possibility
                            page_changed = True
                            print("Row: ", row+1, "Column: ", col+1, " ====> ", possibility)
                            return page_changed, page

    # Col Check
    for col in range(BOARD_SIZE):
        col_candidate={}
        for i in range(BOARD_SIZE):
            col_candidate[i+1] = 0
        for row in range(BOARD_SIZE):
            for possibility in possibilities[row][col]:
                col_candidate[possibility] += 1
            
        for num in col_candidate:
            if col_candidate[num] == 1:
                for row in range(BOARD_SIZE):
                    for possibility in possibilities[row][col]:
                        if possibility == num:
                            page[row][col] = possibility
                            page_changed = True
                            print("Row: ", row+1, "Column: ", col+1, " ====> ", possibility)
                            return page_changed, page
                        
    # Box Check
    for i in range(SQUARE_SIZE):
        for j in range(SQUARE_SIZE):
            box_candidate={}
            for candidate in range(BOARD_SIZE):
                box_candidate[candidate+1] = 0
            for row in range(SQUARE_SIZE):
                for col in range(SQUARE_SIZE):
                    for possibility in possibilities[i*SQUARE_SIZE+row][j*SQUARE_SIZE+col]:
                        box_candidate[possibility] += 1

            for num in box_candidate:
                if box_candidate[num] == 1:
                    for row in range(SQUARE_SIZE):
                        for col in range(SQUARE_SIZE):
                            for possibility in possibilities[i*SQUARE_SIZE+row][j*SQUARE_SIZE+col]:
                                if possibility == num:
                                    page[i*SQUARE_SIZE+row][j*SQUARE_SIZE+col] = possibility
                                    page_changed = True
                                    print("Row: ", i*SQUARE_SIZE+row+1, "Column: ", j*SQUARE_SIZE+col+1, " ====> ", possibility)
                                    return page_changed, page

    return page_changed, page

def solve_puzzle (page, depth):
    depth += 1
    print("-"*20)
    print("We are in depth :: ", depth)
    copy_page = []
    for row in page:
        copy_page.append(row.copy())

    conflict = check_conflict(copy_page)
    if conflict:
        return conflict, copy_page
    else:
        page_changed, copy_page = statics_methods(copy_page)
        if page_changed:
            print("STATIC METHOD USED !!!")
            print("-"*20)
            have_conflict, new_page = solve_puzzle(copy_page, depth)
            print("back to depth", depth)
            while not have_conflict:
                if 0 in new_page:
                    have_conflict, new_page =  solve_puzzle(new_page, depth)
                    print("back to depth", depth)
                else:
                    return have_conflict, new_page
            return True, new_page
        
        else:
            possibilities = check_possibilities(copy_page)
            node_list = []
            possibilities_list = []
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    node_list.append((row, col))
                    possibilities_list.append(len(possibilities[row][col]))

                    sort_list = sorted(range(len(possibilities_list)), key=lambda k: possibilities_list[k])
            
            for item in sort_list:
                row, col = node_list[item]
                if copy_page[row][col] == 0:
                    for possibility in possibilities[row][col]:
                        copy_page[row][col] = possibility
                        if len(possibilities[row][col]) == 1:
                            print("Row: ", row+1, "Column: ", col+1, " ====> ", possibility)
                            print("ONLY ONE CHOICE EXIST !!!")
                            print("-"*20)
                        else:
                            print("Row: ", row+1, "Column: ", col+1, " ====> ", possibility)
                            print("PROBABILISTIC METHOD USED !!!")
                            print("-"*20)
                        have_conflict, new_page = solve_puzzle(copy_page, depth)
                        print("back to depth", depth)
                        while not have_conflict:
                            if 0 in new_page:
                                have_conflict, new_page =  solve_puzzle(new_page, depth)
                                print("back to depth", depth)
                            else:
                                return have_conflict, new_page
                    return True, copy_page
            return False, copy_page
        
if __name__ == "__main__":
    
    # 3*3
    # page = [
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # ]


    # 4*4
    # page = [
    #     [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    #     [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    #     [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    #     [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    #     [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    #     [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    #     [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    #     [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    #     [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    #     [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    #     [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    #     [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    #     [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    #     [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    #     [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    #     [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    # ]

    # Test 4*4
    # page = [
    #     [8, 00, 00, 00, 13, 12, 3, 2, 15, 7, 14, 6, 00, 10, 00, 00],
    #     [00, 00, 00, 12, 00, 00, 8, 9, 00, 3, 00, 00, 00, 15, 1, 00],
    #     [11, 00, 00, 16, 1, 00, 15, 10, 00, 12, 13, 00, 6, 8, 00, 9],
    #     [15, 13, 2, 10, 00, 00, 11, 00, 16, 9, 00, 8, 5, 12, 00, 00],
    #     [16, 10, 8, 00, 00, 00, 7, 12, 00, 5, 00, 13, 1, 00, 00, 14],
    #     [00, 00, 00, 00, 11, 16, 00, 3, 10, 00, 00, 00, 12, 9, 8, 15],
    #     [00, 5, 12, 3, 00, 00, 14, 00, 8, 15, 00, 00, 2, 00, 00, 00],
    #     [9, 11, 00, 14, 00, 8, 2, 00, 12, 1, 7, 00, 00, 00, 13, 00],
    #     [00, 14, 00, 6, 00, 00, 00, 00, 00, 4, 5, 00, 9, 00, 15, 2],
    #     [00, 00, 13, 11, 00, 14, 16, 15, 7, 10, 8, 00, 3, 00, 00, 6],
    #     [2, 12, 10, 00, 5, 00, 4, 6, 9, 00, 16, 15, 7, 00, 00, 11],
    #     [1, 00, 3, 4, 7, 00, 00, 00, 00, 14, 00, 12, 00, 00, 00, 00],
    #     [10, 8, 00, 00, 15, 2, 00, 13, 4, 6, 00, 00, 00, 00, 00, 00],
    #     [12, 00, 9, 00, 00, 4, 00, 7, 00, 11, 00, 2, 00, 3, 10, 00],
    #     [00, 00, 00, 00, 00, 00, 9, 5, 00, 16, 00, 10, 15, 6, 7, 1],
    #     [00, 00, 7, 00, 00, 1, 10, 16, 00, 00, 00, 00, 11, 00, 00, 00],
    # ]


    # Test 3*3
    page = [
        [0, 0, 0, 0, 5, 0, 0, 8, 0],
        [6, 0, 0, 0, 0, 0, 2, 0, 0],
        [0, 9, 0, 0, 7, 0, 0, 0, 0],
        [2, 0, 0, 3, 0, 0, 4, 0, 0],
        [7, 0, 8, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 9],
        [0, 0, 5, 0, 0, 0, 0, 7, 0],
        [0, 4, 0, 6, 0, 0, 0, 0, 0],
        [0, 0, 0, 9, 0, 0, 0, 0, 0]
    ]

    is_failed, answer = solve_puzzle(page, 0)

    if not is_failed:
        print("-"*50)
        for row in answer:
            for index in row:
                print (index, end = ' ')
            print()
        print("-"*50)
    else:
        print("This input board is not solvable !")
