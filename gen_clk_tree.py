from graphviz import Digraph


def prime_factor(n:int, **kwargs):
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


def clk_tree_grap(clk_tree_dict:dict, clk_tree_name:str):
    clk_tree = Digraph(name="clk_tree", format="png")
 
    clk_tree.attr('graph', rankdir='LR')

    stack = []
    stack.append((clk_tree_dict, "pll"))
    while stack:
        _current_dict, _father = stack.pop()
        for __k, __v in _current_dict.items():
            __self_name = f"{_father}_{__k}"
            if isinstance(__v, int):
                __self_label = f"{__k}: {__v}"
            elif isinstance(__v, dict):
                __self_label = f"{__k}"
                stack.append((__v, __self_name))
            clk_tree.node(name=__self_name, label=__self_label)
            clk_tree.edge(tail_name=_father, head_name=__self_name)
    
    clk_tree.save(filename=clk_tree_name, directory=".")
    clk_tree.render(filename=clk_tree_name, view=0, cleanup=1)


def gen_clk_tree_4(prediv_dict:dict):
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
                    _current_dict[___clk_name] = prediv_dict[___clk_name]
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



def gen_clk_tree_24(prediv_dict:dict):
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
                    _current_dict[___clk_name] = prediv_dict[___clk_name]
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


def gen_clk_tree_2(prediv_dict: dict):
    tree_dict = prediv_dict.copy()
    
    # deep first traversal
    first_level_keep2 = True
    stack = []
    stack.append(tree_dict)
    while stack:
        _current_dict = stack.pop()
        
        # get all clk name
        _all_clk_name = [_n for _n in _current_dict.keys()]

        # find if have a div2 node
        _have_div2_node = False
        while _all_clk_name:

            __end_node = []
            __all_clk_div = []
            for ___clk_name in _all_clk_name:
                ___clk_div = _current_dict[___clk_name]
                if ___clk_div == 1:
                    __end_node.append(___clk_name)
                    continue

                __all_clk_div.extend(set(prime_factor_with4(___clk_div, keep2=first_level_keep2)))

            # exclude end node
            for ___clk_name in __end_node:
                _all_clk_name.remove(___clk_name)

            if not _all_clk_name:
                break
            
            # find most popular facotr as clk tree node
            __popular = max(__all_clk_div, key=__all_clk_div.count)

            if __popular == 2:
                _have_div2_node = True
                break
            
            # delete __popular div node
            __end_node = []
            for ___clk_name in _all_clk_name:
                if _current_dict[___clk_name] % __popular == 0:
                    __end_node.append(___clk_name)
            
            for ___clk_name in __end_node:
                _all_clk_name.remove(___clk_name)
            
        # get all clk name
        _all_clk_name = [_n for _n in _current_dict.keys()]
        _prime_factor = prime_factor if _have_div2_node else prime_factor_with4

        # generate clk tree node for all clk
        while _all_clk_name:
            __end_node = []
            __all_clk_div = []
            for ___clk_name in _all_clk_name:
                ___clk_div = _current_dict[___clk_name]
                if ___clk_div == 1:
                    _current_dict[___clk_name] = prediv_dict[___clk_name]
                    __end_node.append(___clk_name)
                    continue

                __all_clk_div.extend(set(_prime_factor(___clk_div, keep2=first_level_keep2)))

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
            if isinstance(v, int):
                print("-"*lvl, k)
            elif isinstance(v, dict):
                print("-"*lvl, k)
                print_clk_tree(v, lvl+1)
    
    prediv_dict = {"clk_a":8, "clk_b":16, "clk_c":32, "clk_d":64, "clk_e":128, "clk_f": 256, "clk_g": 512, "clk_h":384, "clk_i": 47}
    print(prediv_dict)
    clk_tree_2 = gen_clk_tree_2(prediv_dict)
    clk_tree_24 = gen_clk_tree_24(prediv_dict)
    clk_tree_4 = gen_clk_tree_4(prediv_dict)
    clk_tree_grap(clk_tree_2, "clk_tree_2.png")
    clk_tree_grap(clk_tree_24, "clk_tree_24.png")
    clk_tree_grap(clk_tree_4, "clk_tree_4.png")
