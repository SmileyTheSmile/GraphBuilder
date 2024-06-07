import pydot
import pandas as pd

from typing import Generator, List, Tuple
from sqlalchemy import create_engine
from PIL import Image

if __name__ != "__main__":
    from scripts.settings import *
else:
    from settings import *


def generate_graph(rows: Generator, optimal_nodes: List) -> None:
    graph = pydot.Dot(graph_type="graph", rankdir="BT")
    
    _, row = next(rows)
    graph.add_node(
        pydot.Node(
            int(row[id_row]), 
            label=f"№{int(row[id_row])}\nСумма: {row[earnings_row]}", 
            shape=node_shape,
        )
    )
    
    for _, row in rows:
        row_sum = row[earnings_row]
        row_node_num = int(row[id_row])
        row_parent = int(row[id_parent_row])
        
        node = pydot.Node(
            name=row_node_num, 
            label=f"№{row_node_num}\nСумма: {row_sum}", 
            shape=node_shape,
        )
        edge = pydot.Edge(
            src=row_node_num, 
            dst=row_parent, 
            label=row[probability_row],
        )
            
        graph.add_node(node)
        graph.add_edge(edge)
        
    graph.write(path=f'{output_path}{graph_file_name}_raw.png', format="png")
 

def generate_graphs(rows: Generator, optimal_nodes: List) -> None:
    graph = pydot.Dot(graph_type="graph", rankdir="BT")
    cooler_graph = pydot.Dot(graph_type="graph", rankdir="BT")
    
    _, row = next(rows)
    graph.add_node(
        pydot.Node(
            int(row[id_row]), 
            label=f"№{int(row[id_row])}\nСумма: {row[earnings_row]}", 
            shape=node_shape,
        )
    )
    cooler_graph.add_node(
        pydot.Node(
            int(row[id_row]), 
            label=f"№{int(row[id_row])}\nСумма: {row[final_sum_row]}", 
            shape=node_shape,
            fillcolor=fill_color,
            color=fill_color,
            style="filled"
        )
    )
    
    for _, row in rows:
        row_sum = row[earnings_row]
        row_node_num = int(row[id_row])
        row_parent = int(row[id_parent_row])
        
        node = pydot.Node(
            name=row_node_num, 
            label=f"№{row_node_num}\nСумма: {row_sum}", 
            shape=node_shape,
        )
        edge = pydot.Edge(
            src=row_node_num, 
            dst=row_parent, 
            label=row[probability_row],
        )
        
        cooler_node = pydot.Node(
            name=row_node_num, 
            label=f"№{row_node_num}\nСумма: {row[final_sum_row]}", 
            shape=node_shape,
        )
        cooler_edge = pydot.Edge(
            src=row_node_num, 
            dst=row_parent, 
            label=row[probability_row],
        )
        
        if row[id_row] in optimal_nodes:
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


def get_optimal_path(data: pd.DataFrame, required_year: str) -> Tuple:
    grouped = data.groupby(year_row)

    data_by_year = {}
    years = []

    for year, group in grouped:
        years.append(year)
        data_by_year[year] = group.reset_index(drop=True)
    
    if required_year not in years:
        print("Wrong year")
        return []
    
    required_year_data = data_by_year[required_year]
    max_final_sum_in_last_year = max(required_year_data[final_sum_row])
    last_node_row = required_year_data[required_year_data[final_sum_row] == max_final_sum_in_last_year]
    
    nodes_in_path = [last_node_row[id_row].item()]
    parent = last_node_row[id_parent_row]
    
    while not parent.isna().all():
        current_row = data[data[id_row] == parent.item()]
        nodes_in_path.append(current_row[id_row].item())
        parent = current_row[id_parent_row]
        
    return nodes_in_path


def get_data_csv():
    return pd.read_excel(input_file), get_optimal_path(data, year)


def get_data_postgres():
    engine = create_engine(f"postgresql:///?user={login}&password={password}&database={database}&host={server}&port={port}")
    
    data = pd.read_sql(
        sql = '''
                SELECT id, id_parent, earnings, probability, year 
                FROM earnings_predictions 
            ''', 
        con = engine,
    )
    optimal_nodes = []
    
    return data, optimal_nodes
   

if __name__ == "__main__":
    data, optimal_nodes = get_data_postgres()
    
    rows = data.iterrows()
    
    generate_graph(rows, optimal_nodes)
    resize_graphs()
    