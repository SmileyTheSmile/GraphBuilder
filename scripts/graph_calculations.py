import pydot
import pandas as pd

from typing import Generator, List, Tuple

from scripts.settings import *

from PIL import Image


def generate_graph(rows: Generator, optimal_nodes: List) -> None:
    graph = pydot.Dot(graph_type="graph", rankdir="BT")
    cooler_graph = pydot.Dot(graph_type="graph", rankdir="BT")
    
    _, row = next(rows)
    graph.add_node(
        pydot.Node(
            int(row[node_num_label]), 
            label=f"№{int(row[node_num_label])}\nСумма: {row[sum_label]}", 
            shape=node_shape,
        )
    )
    cooler_graph.add_node(
        pydot.Node(
            int(row[node_num_label]), 
            label=f"№{int(row[node_num_label])}\nСумма: {row[final_sum_label]}", 
            shape=node_shape,
            fillcolor=fill_color,
            color=fill_color,
            style="filled"
        )
    )
    
    for _, row in rows:
        row_sum = row[sum_label]
        row_node_num = int(row[node_num_label])
        row_parent = int(row[parent_label])
        
        node = pydot.Node(
            name=row_node_num, 
            label=f"№{row_node_num}\nСумма: {row_sum}", 
            shape=node_shape,
        )
        edge = pydot.Edge(
            src=row_node_num, 
            dst=row_parent, 
            label=row[probability_label],
        )
        
        cooler_node = pydot.Node(
            name=row_node_num, 
            label=f"№{row_node_num}\nСумма: {row[final_sum_label]}", 
            shape=node_shape,
        )
        cooler_edge = pydot.Edge(
            src=row_node_num, 
            dst=row_parent, 
            label=row[probability_label],
        )
        
        if row[node_num_label] in optimal_nodes:
            cooler_node.set_style("filled")
            cooler_node.set_fillcolor(fill_color)
            cooler_node.set_color(fill_color)
            if row_parent in optimal_nodes:
                cooler_edge.set_color(fill_color)
                cooler_edge.set_penwidth(edge_width)
            
        graph.add_node(node)
        graph.add_edge(edge)
            
        cooler_graph.add_node(cooler_node)
        cooler_graph.add_edge(cooler_edge)
        
    graph.write(path=f'{output_path}{graph_file_name}_raw', format="png")
    cooler_graph.write(path=f'{output_path}{cooler_graph_file_name}_raw', format="png")
 
 
def resize_graphs() -> None:
    img = Image.open(f'{output_path}{graph_file_name}_raw')
    img = img.resize((int(img.size[0] / 2), int(img.size[1] / 2)), Image.Resampling.LANCZOS)
    img.save(f'{output_path}{graph_file_name}')
    
    img = Image.open(f'{output_path}{cooler_graph_file_name}_raw')
    img = img.resize((int(img.size[0] / 2), int(img.size[1] / 2)), Image.Resampling.LANCZOS)
    img.save(f'{output_path}{cooler_graph_file_name}')

   
def get_optimal_path(input_file: str, required_year: str) -> Tuple:
    data = pd.read_excel(input_file)
    
    grouped = data.groupby(year_label)

    data_by_year = {}
    years = []

    for year, group in grouped:
        years.append(year)
        data_by_year[year] = group.reset_index(drop=True)
    
    if required_year not in years:
        print("Wrong year")
        return []
    
    required_year_data = data_by_year[required_year]
    max_final_sum_in_last_year = max(required_year_data[final_sum_label])
    last_node_row = required_year_data[required_year_data[final_sum_label] == max_final_sum_in_last_year]
    
    nodes_in_path = [last_node_row[node_num_label].item()]
    parent = last_node_row[parent_label]
    
    while not parent.isna().all():
        current_row = data[data[node_num_label] == parent.item()]
        nodes_in_path.append(current_row[node_num_label].item())
        parent = current_row[parent_label]
        
    return data.iterrows(), nodes_in_path


if __name__ == "__main__":
    generate_graph(*get_optimal_path(input_file, year))
    resize_graphs()
    