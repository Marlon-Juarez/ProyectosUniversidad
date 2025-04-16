from graphviz import Digraph

# Create a new directed graph
dot = Digraph(name='TrafficLightsPetriNet')
dot.attr(rankdir='LR')

# Graph attributes
dot.attr(fontname='Helvetica,Arial,sans-serif')
dot.attr(label='Petri Net Model: T-Intersection Traffic Lights\nHorizontal Direction Control')
dot.attr(fontsize='12')

# Node attributes
dot.attr('node', fontname='Helvetica,Arial,sans-serif')
dot.attr('edge', fontname='Helvetica,Arial,sans-serif')

# Places (circles) - Only for horizontal directions
places = {
    # Principal direction (main road)
    'red_main': 'Red Main',
    'yellow_main': 'Yellow 1',
    'green_main': 'Green 1',
    # Secondary direction (side road)
    'red_sec': 'Red 2',
    'yellow_sec': 'Yellow 2',
    'green_sec': 'Green 2',
    # Safety places
    'safe_main': 'Safe Main',
    'safe_sec': 'Safe 2'
}

# Add places
for p_id, p_label in places.items():
    dot.node(p_id, p_label, shape='circle', fixedsize='true', width='0.9')

# Transitions (boxes)
transitions = {
    # Main direction transitions
    'main_r_to_g': 'Red→Green Main',
    'main_g_to_y': 'Green→Yellow Main',
    'main_y_to_r': 'Yellow→Red Main',
    # Secondary direction transitions
    'sec_r_to_g': 'Red→Green Secondary',
    'sec_g_to_y': 'Green→Yellow Secondary',
    'sec_y_to_r': 'Yellow→Red Secondary'
}

# Add transitions
for t_id, t_label in transitions.items():
    dot.node(t_id, t_label, shape='box')

# Add edges for Main direction
dot.edge('red_main', 'main_r_to_g')
dot.edge('main_r_to_g', 'green_main')
dot.edge('green_main', 'main_g_to_y')
dot.edge('main_g_to_y', 'yellow_main')
dot.edge('yellow_main', 'main_y_to_r')
dot.edge('main_y_to_r', 'red_main')
dot.edge('main_y_to_r', 'safe_sec')  # Safety connection

# Add edges for Secondary direction
dot.edge('red_sec', 'sec_r_to_g')
dot.edge('sec_r_to_g', 'green_sec')
dot.edge('green_sec', 'sec_g_to_y')
dot.edge('sec_g_to_y', 'yellow_sec')
dot.edge('yellow_sec', 'sec_y_to_r')
dot.edge('sec_y_to_r', 'red_sec')
dot.edge('sec_y_to_r', 'safe_main')  # Safety connection

# Safety connections
dot.edge('safe_main', 'main_r_to_g')
dot.edge('safe_sec', 'sec_r_to_g')

# Initial marking (tokens)
# Add initial state markers
dot.node('init_main', '', shape='point')
dot.edge('init_main', 'red_main')
dot.node('init_sec', '', shape='point')
dot.edge('init_sec', 'red_sec')

# Render the graph
dot.render('traffic_lights_t_intersection', format='png', cleanup=True)
