from flask import Flask, render_template, request, jsonify
import heapq
import json
import random

app = Flask(__name__)

# Nodes list with Jalandhar-specific names and spaced-out coordinates for display
nodes = [
    {"id": 1, "name": "Jalandhar Civil Hospital", "x": 300, "y": 100, "type": "hospital"},
    {"id": 2, "name": "Model Town", "x": 450, "y": 150},
    {"id": 3, "name": "Rama Mandi", "x": 600, "y": 100},
    {"id": 4, "name": "Nakodar Road", "x": 750, "y": 150},
    {"id": 5, "name": "BMC Chowk", "x": 250, "y": 250},
    {"id": 6, "name": "Lajpat Nagar", "x": 400, "y": 300},
    {"id": 7, "name": "Guru Nanak Pura", "x": 550, "y": 250},
    {"id": 8, "name": "Urban Estate", "x": 700, "y": 300},
    {"id": 9, "name": "Railway Station", "x": 200, "y": 400},
    {"id": 10, "name": "Industrial Area", "x": 350, "y": 450},
    {"id": 11, "name": "PPR Market", "x": 500, "y": 400},
    {"id": 12, "name": "Basti Sheikh", "x": 650, "y": 450},
    {"id": 13, "name": "Kapoor Hospital", "x": 800, "y": 400},
    {"id": 14, "name": "Adarsh Nagar", "x": 250, "y": 550},
    {"id": 15, "name": "GT Road", "x": 400, "y": 500},
    {"id": 16, "name": "Shastri Nagar", "x": 550, "y": 550},
    {"id": 17, "name": "Mota Singh Nagar", "x": 700, "y": 500},
    {"id": 18, "name": "Leather Complex", "x": 850, "y": 550},
    {"id": 19, "name": "Wadala Chowk", "x": 300, "y": 650},
    {"id": 20, "name": "Bus Stand", "x": 450, "y": 700}
]

# Edges remain unchanged for calculation purposes
edges = [
    {"from": 1, "to": 2, "weight": 2.5},
    {"from": 1, "to": 5, "weight": 3.2},
    {"from": 2, "to": 3, "weight": 2.7},
    {"from": 2, "to": 6, "weight": 3.1},
    {"from": 3, "to": 4, "weight": 2.6},
    {"from": 3, "to": 7, "weight": 2.5},
    {"from": 4, "to": 8, "weight": 3.2},
    {"from": 5, "to": 6, "weight": 2.1},
    {"from": 5, "to": 9, "weight": 3.5},
    {"from": 6, "to": 7, "weight": 2.3},
    {"from": 6, "to": 10, "weight": 2.4},
    {"from": 7, "to": 8, "weight": 2.7},
    {"from": 7, "to": 11, "weight": 2.8},
    {"from": 8, "to": 12, "weight": 2.9},
    {"from": 8, "to": 13, "weight": 2.5},
    {"from": 9, "to": 10, "weight": 2.2},
    {"from": 9, "to": 14, "weight": 3.0},
    {"from": 10, "to": 11, "weight": 2.6},
    {"from": 10, "to": 15, "weight": 1.9},
    {"from": 11, "to": 12, "weight": 2.4},
    {"from": 11, "to": 16, "weight": 3.1},
    {"from": 12, "to": 13, "weight": 2.5},
    {"from": 12, "to": 17, "weight": 2.0},
    {"from": 13, "to": 18, "weight": 3.3},
    {"from": 14, "to": 15, "weight": 2.3},
    {"from": 14, "to": 19, "weight": 1.8},
    {"from": 15, "to": 16, "weight": 2.7},
    {"from": 15, "to": 19, "weight": 2.8},
    {"from": 16, "to": 17, "weight": 2.9},
    {"from": 16, "to": 20, "weight": 2.6},
    {"from": 17, "to": 18, "weight": 2.4},
    {"from": 17, "to": 20, "weight": 3.2},
    {"from": 19, "to": 20, "weight": 2.3},
    {"from": 2, "to": 5, "weight": 2.7},
    {"from": 3, "to": 6, "weight": 3.0},
    {"from": 4, "to": 7, "weight": 3.3},
    {"from": 6, "to": 9, "weight": 2.9},
    {"from": 7, "to": 10, "weight": 3.1},
    {"from": 8, "to": 11, "weight": 2.8},
    {"from": 10, "to": 14, "weight": 3.5},
    {"from": 11, "to": 15, "weight": 2.6},
    {"from": 12, "to": 16, "weight": 3.4},
    {"from": 15, "to": 18, "weight": 3.2}
]

def create_graph_from_edges(edges):
    graph = {}
    for node in nodes:
        graph[node["id"]] = {}
    for edge in edges:
        from_node = edge["from"]
        to_node = edge["to"]
        weight = edge["weight"]
        graph[from_node][to_node] = weight
        graph[to_node][from_node] = weight
    return graph

def dijkstra(graph, start_id, end_id):
    pq = [(0, start_id)]
    distances = {node_id: float('infinity') for node_id in graph}
    distances[start_id] = 0
    previous = {node_id: None for node_id in graph}
    visited = set()
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        if current_node == end_id or current_node in visited:
            continue
        visited.add(current_node)
        for neighbor, weight in graph[current_node].items():
            if neighbor in visited:
                continue
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    
    path = []
    current = end_id
    while current:
        path.insert(0, current)
        current = previous[current]
    
    if path and path[0] != start_id:
        return None, float('infinity')
    return path, distances[end_id]

current_graph = create_graph_from_edges(edges)
current_edges = edges.copy()

@app.route('/')
def index():
    return render_template('index.html', nodes=json.dumps(nodes), edges=json.dumps(current_edges))

@app.route('/find_route', methods=['POST'])
def find_route():
    data = request.get_json()
    start_id = int(data.get('start'))
    end_id = int(data.get('end'))
    
    if start_id == end_id:
        return jsonify({'success': False, 'message': 'Start and end points must be different'})
    
    path, distance = dijkstra(current_graph, start_id, end_id)
    
    if not path or distance == float('infinity'):
        return jsonify({'success': False, 'message': 'No path found to Jalandhar Civil Hospital'})
    
    estimated_time = distance * 1.5
    
    return jsonify({
        'success': True,
        'path': path,
        'distance': distance,
        'time': estimated_time,
        'intersections': len(path) - 2 if len(path) >= 2 else 0
    })

@app.route('/add_traffic', methods=['POST'])
def add_traffic():
    global current_graph, current_edges
    traffic_edges = []
    for edge in edges:
        traffic_factor = random.uniform(1.0, 3.0)
        traffic_edges.append({
            "from": edge["from"],
            "to": edge["to"],
            "weight": edge["weight"] * traffic_factor,
            "traffic": "high" if traffic_factor > 2 else "medium" if traffic_factor > 1.5 else "low"
        })

    current_edges = traffic_edges
    current_graph = create_graph_from_edges(traffic_edges)
    return jsonify({'success': True, 'traffic_edges': traffic_edges})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')