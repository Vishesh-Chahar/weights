import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class ValveSystem:
    def __init__(self, initial_amount, num_layers=3):
        self.num_layers = num_layers
        self.initial_amount = initial_amount
        
        # Calculate sizes - linear increase in valves per layer
        self.num_valves = sum(i for i in range(1, num_layers + 1))  # 1 + 2 + 3 + ... + num_layers
        self.percentages = [0] * self.num_valves
        
        # For each valve we store its input and two outputs
        self.valve_data = {}  # Will store {valve_id: (input, out1, out2)}
        
    def reset_outputs(self):
        """Reset all valve data"""
        self.valve_data.clear()
        # Set initial input
        self.valve_data[0] = (self.initial_amount, 0, 0)

    def _valve(self, x, percent):
        """Split input amount according to percentage"""
        x1 = percent * x / 100
        x2 = x - x1
        return x1, x2

    def process_flow(self):
        """Process the flow through all valves"""
        self.reset_outputs()
        
        # Process each layer
        valve_id = 0
        for layer in range(self.num_layers):
            valves_in_layer = layer + 1  # Linear increase
            
            # Process each valve in current layer
            for i in range(valves_in_layer):
                # Calculate input for this valve
                if layer == 0:
                    input_amount = self.initial_amount
                else:
                    # Get input from upper layer
                    prev_layer_start = sum(l for l in range(layer))
                    if i == 0:  # Leftmost valve
                        parent = prev_layer_start
                        input_amount = self.valve_data[parent][1]  # First output
                    elif i == valves_in_layer - 1:  # Rightmost valve
                        parent = prev_layer_start + layer - 1
                        input_amount = self.valve_data[parent][2]  # Second output
                    else:  # Middle valves
                        left_parent = prev_layer_start + i - 1
                        right_parent = prev_layer_start + i
                        # Combine adjacent outputs from parents
                        input_amount = (self.valve_data[left_parent][2] + 
                                      self.valve_data[right_parent][1])
                
                # Process valve
                out1, out2 = self._valve(input_amount, self.percentages[valve_id])
                self.valve_data[valve_id] = (input_amount, out1, out2)
                valve_id += 1
        
        return self.valve_data

    def get_outputs(self):
        """Get current outputs"""
        return self.valve_data

    def set_percentage(self, index, percent):
        """Set the percentage for a specific valve"""
        if 0 <= index < len(self.percentages):
            self.percentages[index] = percent

def draw_valve_system(system):
    # Create figure with a specific size and add axes for the graph
    fig, ax = plt.subplots(figsize=(12, 8))
    
    G = nx.Graph()
    pos = {}
    labels = {}
    edges = []
    edge_widths = []
    node_sizes = []
    node_colors = []
    
    # Position nodes layer by layer
    y_spacing = 1
    x_spacing = 1
    valve_id = 0
    
    # Color map for flow intensity
    def get_color(value, max_val):
        intensity = min(value / max_val, 1.0)
        return plt.cm.Blues(0.3 + 0.7 * intensity)
    
    # Get max flow for scaling
    max_flow = system.initial_amount
    
    # Draw valves
    for layer in range(system.num_layers):
        valves_in_layer = layer + 1
        
        for i in range(valves_in_layer):
            # Calculate position
            x = (i - valves_in_layer/2 + 0.5) * x_spacing * 2
            y = -layer * y_spacing
            
            # Add valve node
            G.add_node(valve_id)
            pos[valve_id] = (x, y)
            
            # Get valve data
            if valve_id in system.valve_data:
                input_val, out1, out2 = system.valve_data[valve_id]
                # Scale node size by input amount
                node_sizes.append(1000 + 1000 * (input_val / max_flow))
                # Color node by input amount
                node_colors.append(get_color(input_val, max_flow))
                # Show percentage instead of values
                percent = system.percentages[valve_id]
                labels[valve_id] = f"{percent}%"
            
            # Add edges to parent(s)
            if layer > 0:
                prev_layer_start = sum(l for l in range(layer))
                if i == 0:  # Leftmost valve
                    parent = prev_layer_start
                    edges.append((valve_id, parent))
                    edge_widths.append(3 * (system.valve_data[valve_id][0] / max_flow))
                elif i == valves_in_layer - 1:  # Rightmost valve
                    parent = prev_layer_start + layer - 1
                    edges.append((valve_id, parent))
                    edge_widths.append(3 * (system.valve_data[valve_id][0] / max_flow))
                else:  # Middle valves
                    left_parent = prev_layer_start + i - 1
                    right_parent = prev_layer_start + i
                    edges.append((valve_id, left_parent))
                    edges.append((valve_id, right_parent))
                    flow = system.valve_data[valve_id][0] / 2
                    edge_widths.extend([3 * (flow / max_flow)] * 2)
            
            # If this is the last layer, add output nodes
            if layer == system.num_layers - 1:
                output_id_1 = f"out_{valve_id}_1"
                output_id_2 = f"out_{valve_id}_2"
                
                # Add output nodes
                G.add_node(output_id_1)
                G.add_node(output_id_2)
                
                # Position output nodes
                x_left = x - x_spacing/2
                x_right = x + x_spacing/2
                y_out = y - y_spacing
                
                pos[output_id_1] = (x_left, y_out)
                pos[output_id_2] = (x_right, y_out)
                
                # Style output nodes
                node_sizes.extend([800 + 800 * (out1 / max_flow), 
                                 800 + 800 * (out2 / max_flow)])
                node_colors.extend([get_color(out1, max_flow), 
                                  get_color(out2, max_flow)])
                
                # Add output labels
                labels[output_id_1] = f"{out1:.1f}"
                labels[output_id_2] = f"{out2:.1f}"
                
                # Connect to valve
                edges.extend([(output_id_1, valve_id), (output_id_2, valve_id)])
                edge_widths.extend([3 * (out1 / max_flow), 3 * (out2 / max_flow)])
            
            valve_id += 1
    
    # Draw edges (pipes) first
    nx.draw_networkx_edges(G, pos, 
                          edgelist=edges,
                          width=edge_widths,
                          edge_color='lightblue',
                          alpha=0.7,
                          ax=ax)
    
    # Draw nodes (valves and outputs)
    nx.draw_networkx_nodes(G, pos,
                          node_size=node_sizes,
                          node_color=node_colors,
                          edgecolors='gray',
                          linewidths=2,
                          ax=ax)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, labels,
                           font_size=8,
                           font_weight='bold',
                           ax=ax)
    
    ax.set_title("Valve System Flow")
    
    # Add a colorbar
    sm = plt.cm.ScalarMappable(cmap=plt.cm.Blues, 
                              norm=plt.Normalize(vmin=0, vmax=max_flow))
    plt.colorbar(sm, ax=ax, label='Flow Amount')
    
    # Remove axis
    ax.set_axis_off()
    
    return fig

def main():
    st.title("Neural Network Weights Simulator")
    
    # Configuration inputs
    col1, col2 = st.columns(2)
    with col1:
        initial_amount = st.number_input("Initial Amount", value=1000, min_value=0)
    with col2:
        num_layers = st.number_input("Number of Layers", value=3, min_value=1, max_value=5)
    
    # Create valve system
    system = ValveSystem(initial_amount, num_layers)
    
    # Create select sliders for valve percentages
    st.subheader("Valve Percentages (Weights)")
    
    # Define steps for the select slider
    percent_options = list(range(0, 101, 5))  # [0, 5, 10, ..., 95, 100]
    
    # Organize inputs by layer
    valve_id = 0
    for layer in range(num_layers):
        st.write(f"Layer {layer + 1}")
        valves_in_layer = layer + 1
        cols = st.columns(valves_in_layer)
        
        for i in range(valves_in_layer):
            with cols[i]:
                value = st.select_slider(
                    f"V{i+1}",
                    options=percent_options,
                    value=0,
                    key=f"valve_{valve_id}",
                    format_func=lambda x: f"{x}%"
                )
                system.set_percentage(valve_id, value)
                valve_id += 1
    
    # Process flow and show visualization
    results = system.process_flow()
    
    # Display visualization
    st.subheader("System Visualization")
    fig = draw_valve_system(system)
    st.pyplot(fig)
    plt.close()

if __name__ == "__main__":
    main()
