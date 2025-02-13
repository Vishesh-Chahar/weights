# Valve System Simulator

A Streamlit-based interactive visualization tool for simulating and analyzing fluid flow through a configurable network of valves.

## Description

This application simulates fluid flow through a hierarchical system of valves, where each valve splits the incoming flow into two outputs based on user-defined percentages. The system visualizes the flow using an interactive network graph with color-coded nodes and weighted edges representing flow intensity.

## Features

- **Configurable System Parameters**
  - Adjustable initial flow amount
  - Variable number of layers (1-5)
  - Individual valve control with percentage-based split ratios

- **Interactive Visualization**
  - Color-coded nodes representing flow intensity
  - Weighted edges showing flow distribution
  - Node sizes proportional to flow amount
  - Clear percentage labels on valves
  - Output values displayed at terminal nodes

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
```

2. Install required dependencies:
```bash
pip install streamlit numpy networkx matplotlib
```

3. Run the application:
```bash
streamlit run streamlit_weights.py
```

## Usage

1. Set the initial flow amount using the number input
2. Choose the number of layers (1-5)
3. Adjust valve percentages using the sliders
   - Each percentage determines how much flow goes to the left output
   - The remaining flow automatically goes to the right output
4. The visualization updates automatically to show flow distribution

## How It Works

- Each valve splits the incoming flow into two outputs based on the set percentage
- Flow is distributed layer by layer from top to bottom
- Middle valves in each layer receive combined input from two parent valves
- The visualization uses:
  - Node size to represent flow amount
  - Color intensity to indicate flow strength
  - Edge thickness to show flow volume between nodes

## Dependencies

- Streamlit
- NumPy
- NetworkX
- Matplotlib

## License

MIT License

## Authors

Vishesh Chahar (https://github.com/Vishesh-Chahar)


This README provides a comprehensive overview of your project, including installation instructions, usage guidelines, and technical details. You may want to customize the sections marked with brackets ([ ]) with specific information for your project, such as the repository URL, license details, and author information.

The README is structured to be both informative for users who want to use the application and helpful for developers who might want to understand or contribute to the code.
