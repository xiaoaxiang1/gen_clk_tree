def prime_factor(n:int):
    res_list = []
    while n != 1:
        for i in range(2, n+1):
            if n % i == 0:
                res_list.append(i)
                n = n // i
                break
    return res_list

def gen_clk_tree_4(prediv_dict:dict):
    def prime_factor(n:int):
        res_list = []
        while n != 1:
            for i in range(2, n+1):
                if n % i == 0:
                    res_list.append(i)
                    n = n // i
                    break
        return res_list
    
    def prime_factor_with4(n:int, keep2:bool=False):
        assert n > 1
        res_list = []
        # divide by 4
        while n % 4 == 0:
            res_list.append(4)
            n = n // 4
        
        if n != 1:
            res_list.extend(prime_factor(n))
        
        if keep2 and (not 2 in res_list) and (4 in res_list):
            res_list.remove(4)
            res_list.extend([2, 2])
        
        res_list.sort()
        
        return res_list
    
    # calc prime factor
    tree_dict = {}
    for _k, _v in prediv_dict.items():
        tree_dict[_k] = prime_factor_with4(_v, keep2=True)
    
    # deep first traversal
    stack = []
    stack.append(tree_dict)
    while stack:
        _current_dict = stack.pop()

        # get all clk name
        _all_clk_name = [_n for _n in _current_dict.keys()]

        # generate clk tree node for all clk
        while _all_clk_name:
            __end_node = []
            __all_clk_div = []
            for ___clk_name in _all_clk_name:
                if len(_current_dict[___clk_name]) == 0:
                    _current_dict[___clk_name] = 1
                    __end_node.append(___clk_name)
                    continue

                __all_clk_div.extend(set(_current_dict[___clk_name]))
            
            # exclude end node
            for ___clk_name in __end_node:
                _all_clk_name.remove(___clk_name)

            if not _all_clk_name:
                break
            
            # find most popular facotr as clk tree node
            __popular = max(__all_clk_div, key=__all_clk_div.count)
            __new_dict = {}
            
            # put clk to new branch and delete it in current dict
            for ___clk_name in _all_clk_name:
                if __popular in _current_dict[___clk_name]:
                    _current_dict[___clk_name].remove(__popular)
                    __new_dict[___clk_name] = _current_dict[___clk_name]
                    _current_dict.pop(___clk_name)
            
            for ___clk_name in __new_dict.keys():
                _all_clk_name.remove(___clk_name)
            
            # put new branch to current dict
            _current_dict[__popular] = __new_dict

            # push new branch to stack
            stack.append(__new_dict)
    
    return tree_dict



def gen_clk_tree_2(prediv_dict:dict):
    def prime_factor(n:int):
        assert n > 1
        res_list = []
        while n != 1:
            for i in range(2, n+1):
                if n % i == 0:
                    res_list.append(i)
                    n = n // i
                    break
        return res_list
    
    def prime_factor_with4(n:int, keep2:bool=False):
        assert n > 1
        res_list = []
        # divide by 4
        while n % 4 == 0:
            res_list.append(4)
            n = n // 4
        
        if n != 1:
            res_list.extend(prime_factor(n))
        
        if keep2 and (not 2 in res_list) and (4 in res_list):
            res_list.remove(4)
            res_list.extend([2, 2])
        
        res_list.sort()
        
        return res_list
    
    tree_dict = prediv_dict.copy()
    
    # deep first traversal
    first_level_keep2 = True
    stack = []
    stack.append(tree_dict)
    while stack:
        _current_dict = stack.pop()

        # get all clk name
        _all_clk_name = [_n for _n in _current_dict.keys()]

        # generate clk tree node for all clk
        while _all_clk_name:
            __end_node = []
            __all_clk_div = []
            for ___clk_name in _all_clk_name:
                ___clk_div = _current_dict[___clk_name]
                if ___clk_div == 1:
                    __end_node.append(___clk_name)
                    continue

                __all_clk_div.extend(set(prime_factor_with4(___clk_div, first_level_keep2)))

            # exclude end node
            for ___clk_name in __end_node:
                _all_clk_name.remove(___clk_name)

            if not _all_clk_name:
                break
            
            # find most popular facotr as clk tree node
            __popular = max(__all_clk_div, key=__all_clk_div.count)
            __new_dict = {}
            
            # put clk to new branch and delete it in current dict
            for ___clk_name in _all_clk_name:
                if _current_dict[___clk_name] % __popular == 0:
                    __new_dict[___clk_name] = _current_dict[___clk_name] // __popular
                    _current_dict.pop(___clk_name)
            
            for ___clk_name in __new_dict.keys():
                _all_clk_name.remove(___clk_name)
            
            # put new branch to current dict
            _current_dict[__popular] = __new_dict

            # push new branch to stack
            stack.append(__new_dict)
        
        first_level_keep2 = False


    return tree_dict


if __name__ == "__main__":
    def print_clk_tree(clk_tree:dict, lvl=0):
        for k,v in clk_tree.items():
            if v == 1:
                print("-"*lvl, k)
            elif isinstance(v, dict):
                print("-"*lvl, k)
                print_clk_tree(v, lvl+1)
    
    prediv_dict = {"clk_a":24, "clk_b":24, "clk_c":64, "clk_d":128}
    print(prediv_dict)
    print_clk_tree(gen_clk_tree_2(prediv_dict))
    print_clk_tree(gen_clk_tree_4(prediv_dict))
