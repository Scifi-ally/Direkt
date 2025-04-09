
**Project Title:** Flask-Based Web Application for Fastest Route Navigation to Jalandhar Civil Hospital

**Description:**  
This project is a dynamic web application developed using Flask that determines the fastest route to **Jalandhar Civil Hospital** from a given location using **Dijkstra’s Algorithm**. The application features an **interactive SVG map** that visually represents the road network, nodes (intersections), and real-time simulated traffic conditions. Each route is computed by taking both **distance** and **traffic delays** into account, allowing for more realistic and practical routing.

**Key Features:**
- **Dijkstra’s Algorithm** for calculating the shortest path based on weighted graph representation.
- **Dynamic Traffic Simulation** that alters edge weights in real-time to mimic traffic congestion and affect route computation accordingly.
- **Interactive SVG Map Interface** where users can:
  - Select starting points manually.
  - View highlighted optimal paths to the destination (Jalandhar Civil Hospital).
  - Hover over or click on roads/nodes to see traffic status or road names.
- **Modular Design** with clear separation between the frontend (HTML/CSS/JS + SVG map) and backend (Flask + Python logic).
- **Scalable**: Easily extendable to include multiple destinations, more cities, or real-time traffic data from APIs in the future.

**Use Cases:**
- Helps emergency services and ambulance drivers find the fastest route to the hospital.
- Useful for urban planning and traffic management simulations.
