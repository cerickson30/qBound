def Glabel(G):
    return G.canonical_label().graph6_string()


##########################################################################################
#################################### Seen Dict ###########################################
##########################################################################################

def write_seen_dict(seen_dict, path_prefix='data'):
    with open(path_prefix + f'/seen_dict_backup.txt', 'w') as outfile:
        outfile.write(str(seen_dict))
        
    # Just in case there's an interuption while the connection is open, make a backup
    with open(path_prefix + f'/seen_dict.txt', 'w') as outfile:
        outfile.write(str(seen_dict))


def get_last_seen_dict_numbers(path_prefix='data'):
    import os
    
    files_list = os.listdir(path_prefix + '/seen_dict')
    max_n = 0
    for filename in files_list:
        if '_verts_' in filename:
            start_idx = filename.find('_dict_') + len('_dict_')
            stop_idx = filename.find('_verts_')
            if int(filename[start_idx:stop_idx]) > max_n:
                max_n = int(filename[start_idx:stop_idx])

    edges = max_n*(max_n - 1) // 2
    for filename in files_list:
        if f'_{max_n}_verts' in filename:
            start_idx = filename.find('_verts_') + len('_verts_')
            try:
                stop_idx = filename.index('_edges-backup.txt')
            except ValueError:
                stop_idx = filename.index('_edges.txt')
            if int(filename[start_idx:stop_idx]) < edges:
                edges = int(filename[start_idx:stop_idx])

    return (max_n, edges)


## Read partial seen_dict for a given number of vertices and edges
def read_partial_seen_dict(num_verts, num_edges, path_prefix='data'):
    try:
        # try the primary file
        with open(f'{path_prefix}/seen_dict/seen_dict_{num_verts}_verts_{num_edges}_edges.txt', 'r') as infile:
            return eval(infile.read())
    except:
        # If primary file is corrupted (empty), try backup
        with open(f'{path_prefix}/seen_dict/seen_dict_{num_verts}_verts_{num_edges}_edges-backup.txt', 'r') as infile:
            return eval(infile.read())
        
        
def write_partial_seen_dict(num_verts, num_edges, seen_dict, path_prefix='data'):
    with open(f'{path_prefix}/seen_dict/seen_dict_{num_verts}_verts_{num_edges}_edges.txt', 'w') as outfile:
        outfile.write(str(seen_dict[f'{num_verts}_verts'][f'{num_edges}_edges']))
    
    # Just in case there's an interuption while the connection is open, make a backup
    with open(f'{path_prefix}/seen_dict/seen_dict_{num_verts}_verts_{num_edges}_edges-backup.txt', 'w') as outfile:
        outfile.write(str(seen_dict[f'{num_verts}_verts'][f'{num_edges}_edges'])) 
        

def init_seen_dict(path_prefix='data'):
    max_n, edcount = get_last_seen_dict_numbers(path_prefix)

    vertex_keys = [f'{nn}_verts' for nn in range(11)]
    seen_dict = dict(zip(vertex_keys, [{} for nn in range(11)]))
    for nn in range(11):
        edge_dict_keys = [f"{ee}_edges" for ee in range(Integer((nn*(nn-1))/2), 0, -1)]
        seen_dict[f"{nn}_verts"] = dict(zip(edge_dict_keys,[set() for ee in range(len(edge_dict_keys))]))

    # add the graph on 0 vertices
    seen_dict['0_verts']['0_edges'] = set(Glabel(Graph(0)))
    # add the graph on 1 vertex
    seen_dict['1_verts']['0_edges'] = set(Glabel(Graph(1)))
    
    if max_n >= 2:
        # add lower vertex number graphs
        for n_verts in range(2, max_n):
            for m_edges in range(n_verts*(n_verts-1)//2, 0, -1):
    #             print(n_verts, m_edges)
                seen_dict[f'{n_verts}_verts'][f'{m_edges}_edges'] = read_partial_seen_dict(n_verts, m_edges, path_prefix)

        # add previously computed for max_n
        for m_edges in range(max_n*(max_n-1)//2, edcount-1, -1):
    #         print(max_n, m_edges)
            seen_dict[f'{max_n}_verts'][f'{m_edges}_edges'] = read_partial_seen_dict(max_n, m_edges, path_prefix)
    
    return seen_dict



##########################################################################################
################################ Completed Dict ##########################################
##########################################################################################

def write_completed_dict(completed_dict, path_prefix='data'):
    with open(path_prefix + f'/completed_dict_backup.txt', 'w') as outfile:
        outfile.write(str(completed_dict))
        
    # Just in case there's an interuption while the connection is open, make a backup
    with open(path_prefix + f'/completed_dict.txt', 'w') as outfile:
        outfile.write(str(completed_dict))


def get_last_completed_dict_numbers(path_prefix='data'):
    import os
    
    files_list = os.listdir(path_prefix + '/completed_dict')
    max_n = 0
    for filename in files_list:
        if '_verts_' in filename:
            start_idx = filename.find('_dict_') + len('_dict_')
            stop_idx = filename.find('_verts_')
            if int(filename[start_idx:stop_idx]) > max_n:
                max_n = int(filename[start_idx:stop_idx])

    edges = max_n*(max_n - 1) // 2
    for filename in files_list:
        if f'_{max_n}_verts' in filename:
            start_idx = filename.find('_verts_') + len('_verts_')
            try:
                stop_idx = filename.index('_edges-backup.txt')
            except ValueError:
                stop_idx = filename.index('_edges.txt')
            if int(filename[start_idx:stop_idx]) < edges:
                edges = int(filename[start_idx:stop_idx])

    return (max_n, edges)


## Read partial seen_dict for a given number of vertices and edges
def read_partial_completed_dict(num_verts, num_edges, path_prefix='data'):
    try:
        # try the primary file
        with open(f'{path_prefix}/completed_dict/completed_dict_{num_verts}_verts_{num_edges}_edges.txt', 'r') as infile:
            return eval(infile.read())
    except:
        # If primary file is corrupted (empty), try backup
        with open(f'{path_prefix}/completed_dict/completed_dict_{num_verts}_verts_{num_edges}_edges-backup.txt', 'r') as infile:
            return eval(infile.read())
        
        
def write_partial_completed_dict(num_verts, num_edges, completed_dict, path_prefix='data'):
    with open(f'{path_prefix}/completed_dict/completed_dict_{num_verts}_verts_{num_edges}_edges.txt', 'w') as outfile:
        outfile.write(str(completed_dict[f'{num_verts}_verts'][f'{num_edges}_edges']))
    
    # Just in case there's an interuption while the connection is open, make a backup
    with open(f'{path_prefix}/completed_dict/completed_dict_{num_verts}_verts_{num_edges}_edges-backup.txt', 'w') as outfile:
        outfile.write(str(completed_dict[f'{num_verts}_verts'][f'{num_edges}_edges'])) 
        

def init_completed_dict(path_prefix='data'):
    max_n, edcount = get_last_completed_dict_numbers(path_prefix)

    vertex_keys = [f'{nn}_verts' for nn in range(11)]
    completed_dict = dict(zip(vertex_keys, [{} for nn in range(11)]))
    for nn in range(11):
        edge_dict_keys = [f"{ee}_edges" for ee in range(Integer((nn*(nn-1))/2), 0, -1)]
        completed_dict[f"{nn}_verts"] = dict(zip(edge_dict_keys,[set() for ee in range(len(edge_dict_keys))]))

    # add the graph on 0 vertices
    completed_dict['0_verts']['0_edges'] = set(Glabel(Graph(0)))
    # add the graph on 1 vertex
    completed_dict['1_verts']['0_edges'] = set(Glabel(Graph(1)))
    
    if max_n >= 2:
        # add lower vertex number graphs
        for n_verts in range(2, max_n):
            for m_edges in range(n_verts*(n_verts-1)//2, 0, -1):
    #             print(n_verts, m_edges)
                completed_dict[f'{n_verts}_verts'][f'{m_edges}_edges'] = read_partial_completed_dict(n_verts, m_edges, path_prefix)

        # add previously computed for max_n
        for m_edges in range(max_n*(max_n-1)//2, edcount-1, -1):
    #         print(max_n, m_edges)
            completed_dict[f'{max_n}_verts'][f'{m_edges}_edges'] = read_partial_completed_dict(max_n, m_edges, path_prefix)
    
    return completed_dict



##########################################################################################
################################ Minimals Dict ###########################################
##########################################################################################

def get_last_minimals_dict_numbers(path_prefix='data'):
    import os
    
    files_list = os.listdir(path_prefix + '/minimals_dict')
    max_n = 0
    for filename in files_list:
        if '_verts_' in filename:
            start_idx = filename.find('_dict_') + len('_dict_')
            stop_idx = filename.find('_verts_')
            if int(filename[start_idx:stop_idx]) > max_n:
                max_n = int(filename[start_idx:stop_idx])

    edges = max_n*(max_n - 1) // 2
    for filename in files_list:
        if f'_{max_n}_verts' in filename:
            start_idx = filename.find('_verts_') + len('_verts_')
            try:
                stop_idx = filename.index('_edges-backup.txt')
            except ValueError:
                stop_idx = filename.index('_edges.txt')
            if int(filename[start_idx:stop_idx]) < edges:
                edges = int(filename[start_idx:stop_idx])

    return (max_n, edges)


def write_minimals_dict(num_verts, num_edges, minimals_dict, path_prefix='data'):
    with open(path_prefix +
              f'/minimals_dict/minimals_dict_{num_verts}_verts_{num_edges}_edges-backup.txt', 'w') as outfile:
        outfile.write(str(minimals_dict))
    
    # Just in case there's an interuption while the connection is open, make a backup
    with open(path_prefix +
              f'/minimals_dict/minimals_dict_{num_verts}_verts_{num_edges}_edges.txt', 'w') as outfile:
        outfile.write(str(minimals_dict))


def read_minimals_dict(path_prefix='data'):
    max_n, edge_count = get_last_minimals_dict_numbers(path_prefix)
    
    try:
        # try the primary file
        with open(path_prefix + f'/minimals_dict/minimals_dict_{num_verts}_verts_{num_edges}_edges.txt', 'r') as infile:
            return eval(infile.read())
    except:
        # If primary file is corrupted (empty), try backup
        try:
            with open(path_prefix + f'/minimals_dict/minimals_dict_{num_verts}_verts_{num_edges}_edges-backup.txt', 'r') as infile:
                return eval(infile.read())
        except:
            # If both seen_dict.txt and seen_dict_backup.txt are corrupted, or don't exist, initialize uspcm_dict
            minimals_dict_keys = [f'{kk}_spectators' for kk in range(10)]
            minimals_dict = dict(zip(minimals_dict_keys, [set() for kk in range(10)]))
            minimals_dict['0_spectators'].add('@')
            
            return minimals_dict        



##########################################################################################
################################### USPCM Dict ###########################################
##########################################################################################

def get_last_uspcm_dict_numbers(path_prefix='data'):
    import os
    
    files_list = os.listdir(path_prefix + '/uspcm_dict')
    max_n = 0
    for filename in files_list:
        if '_verts_' in filename:
            start_idx = filename.find('_dict_') + len('_dict_')
            stop_idx = filename.find('_verts_')
            if int(filename[start_idx:stop_idx]) > max_n:
                max_n = int(filename[start_idx:stop_idx])

    edges = max_n*(max_n - 1) // 2
    for filename in files_list:
        if f'_{max_n}_verts' in filename:
            start_idx = filename.find('_verts_') + len('_verts_')
            try:
                stop_idx = filename.index('_edges-backup.txt')
            except ValueError:
                stop_idx = filename.index('_edges.txt')
            if int(filename[start_idx:stop_idx]) < edges:
                edges = int(filename[start_idx:stop_idx])

    return (max_n, edges)


def write_full_uspcm_dict(uspcm_dict, path_prefix='data'):
    with open(path_prefix + 
              f'/full_uspcm_dict/full_uspcm_dict_backup.txt', 'w') as outfile:
        outfile.write(str(uspcm_dict))
    
    # Just in case there's an interuption while the connection is open, make a backup
    with open(path_prefix + 
              f'/full_uspcm_dict/full_uspcm_dict.txt', 'w') as outfile:
        outfile.write(str(uspcm_dict))
        
        
## Read partial uspcm_dict for a given number of vertices and edges
def read_partial_uspcm_dict(num_verts, num_edges, path_prefix='data'):
    try:
        # try the primary file
        with open(f'{path_prefix}/uspcm_dict/uspcm_dict_{num_verts}_verts_{num_edges}_edges.txt', 'r') as infile:
            return eval(infile.read())
    except:
        # If primary file is corrupted (empty), try backup
        with open(f'{path_prefix}/uspcm_dict/uspcm_dict_{num_verts}_verts_{num_edges}_edges-backup.txt', 'r') as infile:
            return eval(infile.read())
        
        
def write_partial_uspcm_dict(num_verts, num_edges, uspcm_dict, path_prefix='data'):
    with open(f'{path_prefix}/uspcm_dict/uspcm_dict_{num_verts}_verts_{num_edges}_edges.txt', 'w') as outfile:
        outfile.write(str(uspcm_dict[f'{num_verts}_verts'][f'{num_edges}_edges']))
    
    # Just in case there's an interuption while the connection is open, make a backup
    with open(f'{path_prefix}/uspcm_dict/uspcm_dict_{num_verts}_verts_{num_edges}_edges-backup.txt', 'w') as outfile:
        outfile.write(str(uspcm_dict[f'{num_verts}_verts'][f'{num_edges}_edges']))  
        
        
def init_uspcm_dict(path_prefix='data'):
    max_n, edcount = get_last_uspcm_dict_numbers(path_prefix)

    vertex_keys = [f'{nn}_verts' for nn in range(11)]
    uspcm_dict = dict(zip(vertex_keys, [{} for nn in range(11)]))
    for nn in range(11):
        edge_dict_keys = [f'{ee}_edges' for ee in range(Integer((nn*(nn-1))/2), -1, -1)]
        uspcm_dict[f'{nn}_verts'] = dict(zip(edge_dict_keys,[{} for ee in range(len(edge_dict_keys))]))

    # add the graph on 0 vertices
    uspcm_dict['0_verts']['0_edges'] = {Glabel(Graph(0)): 0}
    # add the graph on 1 vertex
    uspcm_dict['1_verts']['0_edges'] = {Glabel(Graph(1)): 0}
    
    if max_n >= 2:
        # add lower vertex number graphs
        for n_verts in range(2, max_n):
            for m_edges in range(n_verts*(n_verts-1)//2, 0, -1):
    #             print(n_verts, m_edges)
                uspcm_dict[f'{n_verts}_verts'][f'{m_edges}_edges'] = read_partial_uspcm_dict(n_verts, m_edges, path_prefix)

        # add previously computed for max_n
        for m_edges in range(max_n*(max_n-1)//2, edcount-1, -1):
    #         print(max_n, m_edges)
            uspcm_dict[f'{max_n}_verts'][f'{m_edges}_edges'] = read_partial_uspcm_dict(max_n, m_edges, path_prefix)
    
    return uspcm_dict



##########################################################################################
############################## Initialize All Dicts ######################################
##########################################################################################

def get_spectator_number_dictionaries(path_prefix='data'):
    """
    INPUT: path_prefix (default = 'data')
    
    OUTPUT: uspcm_dict, minimals_dict, seen_dict, completed_dict
    """
    
    uspcm_dict = init_uspcm_dict(path_prefix)
    minimals_dict = read_minimals_dict(path_prefix)
    seen_dict = init_seen_dict(path_prefix)
    completed_dict = init_completed_dict(path_prefix)
        
    return uspcm_dict, minimals_dict, seen_dict, completed_dict