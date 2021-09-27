def get_full_uspcm_dict():
    """Access the GitHub repo to put together the complete uspcm_dict,
the dictionary of connected graphs on up to 10 vertices (inclusive) with the spectator number for each graph.

This is a nested dictionary, to access, e.g., the dictionary of connected graphs on 6 vertices and 10 edges, use
uspcm_dict['6_verts']['10_edges']. The innermost dictionary's keys are graph6_strings and the values are the spectator
number for that graph."""
    
    import requests

    uspcm_dict = {}
    url_path = 'https://raw.githubusercontent.com/cerickson30/qBound/main/data/uspcm_dict/'


    for num_verts in range(2):
        uspcm_dict[f'{num_verts}_verts'] = {}

        filename = f'uspcm_dict_{num_verts}_verts_{0}_edges.txt'

        file_url = f'{url_path}/{filename}'
        response = response = requests.get(file_url)
        uspcm_dict[f'{num_verts}_verts'][f'{0}_edges'] = eval(response.text)


    for num_verts in range(2, 11):
        uspcm_dict[f'{num_verts}_verts'] = {}

        for num_edges in range(num_verts*(num_verts-1)//2, 0, -1):
            filename = f'uspcm_dict_{num_verts}_verts_{num_edges}_edges.txt'

            file_url = f'{url_path}/{filename}'
            response = response = requests.get(file_url)
            uspcm_dict[f'{num_verts}_verts'][f'{num_edges}_edges'] = eval(response.text)
            
    return uspcm_dict



def get_partial_uspcm_dict(num_verts, num_edges):
    """Access the GitHub repo to get just the part of the uspcm_dict for num_verts vertices and num_edges edges,
    where num_verts is at most 10.

This is a nested dictionary, to access, e.g., the dictionary of connected graphs on 6 vertices and 10 edges, use
uspcm_dict['6_verts']['10_edges']. The innermost dictionary's keys are graph6_strings and the values are the spectator
number for that graph."""
    
    import requests

    uspcm_dict = {}
    url_path = 'https://raw.githubusercontent.com/cerickson30/qBound/main/data/uspcm_dict/'
    filename = f'uspcm_dict_{num_verts}_verts_{num_edges}_edges.txt'

    file_url = f'{url_path}/{filename}'
    response = response = requests.get(file_url)
    
    uspcm_dict[f'{num_verts}_verts'] = {}
    uspcm_dict[f'{num_verts}_verts'][f'{num_edges}_edges'] = eval(response.text)

    return uspcm_dict



def read_minor_minimals():
    """Returns the dictionary of spectator number minor-minimal graphs from the GitHub repo"""
    import requests
    
    url = 'https://raw.githubusercontent.com/cerickson30/qBound/main/data/minimals_dict.txt'
    response = requests.get(url)
    return eval(response.text)



def display_connected_minimal_graphs(spec_num):
    """INPUT: spec_num - the spectator number
    OUTPUT: Prints the connected minor-minimal graphs with spectator number equal to spec_num"""

    minimals_dict = read_minor_minimals()
    
    if spec_num in [5, 6, 7]:
        num = len(minimals_dict[f'{spec_num}_spectators'])
        message = f"""Warning: There are {num} connected minor-minimal graphs on at most 10 vertices with spectator number {spec_num},
are you sure you want to proceed?
Enter 'Yes' to print all {num} of the graphs.\n"""
        response = input(message)
        if response != 'Yes':
            return None
    

    
    graph_list = list(minimals_dict[f'{spec_num}_spectators'])
    nrows = ceil(len(graph_list)/3)
    counter = 0
    while len(graph_list) > 2:

        row = [graph_list.pop(0), graph_list.pop(0), graph_list.pop(0)]
        G1 = Graph(row[0])
        G2 = Graph(row[1])
        G3 = Graph(row[2])
        counter += 3

        ga = graphics_array((G1.plot(title=row[0]), G2.plot(title=row[1]), G3.plot(title=row[2])))
        ga.show(figsize=(15,3))
        print('\n')


    if len(graph_list) == 2:
        row = [graph_list.pop(0), graph_list.pop(0)]
        G1 = Graph(row[0])
        G2 = Graph(row[1])
        counter += 2

        ga = graphics_array((G1.plot(title=row[0]), G2.plot(title=row[1])))
        ga.show(figsize=(15,3))
        print('\n')
    else:
        row = [graph_list.pop(0)]
        G1 = Graph(row[0])
        counter += 1

        G1.show(title=row[0], figsize=(15,3), fontsize=14)
        print('\n')
        
        
        
def get_spectator_floor(graph, uspcm_dict=None):
    """INPUT: graph: A graph, graph6_string, or adjacency matrix for a connected graph on at most 10 vertices
uspcm_dict: A dictionary of spectator floor numbers, either the complete dictionary or partial dictionary with
the spectator floor numbers for graphs on the number of vertices and edges that the graph argument has.
OUTPUT: The spectator floor number of the graph.
    """
    G, g6_str = get_canonical_graph(graph)
        
    if G.num_verts() > 10 or G.is_connected() == False:
        return "This function only works for connected graphs on at most 10 vertices"

    num_verts = G.num_verts()
    num_edges = G.num_edges()
    
    if uspcm_dict is None:
        uspcm_dict = get_partial_uspcm_dict(num_verts, num_edges)

    return uspcm_dict[f'{num_verts}_verts'][f'{num_edges}_edges'][g6_str]



def get_canonical_graph(graph):
    try:
        mat = Matrix(graph)
        G = Graph(mat)
        g6_str = G.canonical_label().graph6_string()
    except TypeError:
        if type(graph) == str:
            G = Graph(graph)
            g6_str = G.canonical_label().graph6_string()
        elif type(graph) == Graph:
            G = graph
            g6_str = G.canonical_label().graph6_string()
            
    return G, g6_str

        

def has_minor(G, H):
    """Determines if graph H is a minor of graph G"""
    g,_ = get_canonical_graph(G)
    h,_ = get_canonical_graph(H)
            
    try:
        m = g.minor(h)
        return True
    except:
        return False
    
    

def find_minimal_representation(graph, uspcm_dict=None, minimals_dict=None):
    """INPUT: graph: A graph, graph6_string, or adjacency matrix for a connected graph on at most 10 vertices
uspcm_dict: A dictionary of spectator floor numbers, either the complete dictionary or partial dictionary with
the spectator floor numbers for graphs on the number of vertices and edges that the graph argument has.
OUTPUT: The spectator floor number of the graph.
    """
    G, g6_str = get_canonical_graph(graph)
        
    if G.num_verts() > 10 or G.is_connected() == False:
        return "This function only works for connected graphs on at most 10 vertices"

    num_verts = G.num_verts()
    num_edges = G.num_edges()
        
    G_spec_floor = get_spectator_floor(g6_str, uspcm_dict)
    
    if minimals_dict is None:
        minimals_dict = read_minor_minimals()
    
    if g6_str in minimals_dict[f'{G_spec_floor}_spectators']:
        print(f'{graph} is minor-minimal, the canonical labelling of {graph} has graph6_string of {g6_str}')
        if type(graph) == Graph:
            graph.show(title = f'G: {g6_str}, spec_floor = {G_spec_floor}')
        else:
            G.show(title = f'G: {g6_str}, spec_floor = {G_spec_floor}')
        return g6_str
    for H_str in minimals_dict[f'{G_spec_floor}_spectators']:
        if has_minor(G, H_str):
            print(f'{H_str} is a minor of {graph}, both have spectator floor of {G_spec_floor}, so {graph} is NOT minor-minimal')
            ga = graphics_array((G.plot(title = f'G: {g6_str}, spec_floor = {G_spec_floor}'),
                                Graph(H_str).plot(title = f'H: {H_str}, spec_floor = {G_spec_floor}')))
            ga.show()
            return H_str