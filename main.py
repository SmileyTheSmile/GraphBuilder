import pandas as pd
import pydot
from typing import Generator, List


# Именя столбцов
parent_label = '№ родителя'
node_num_label = '№ вершины'
probability_label = 'Вероятность'
year_label = 'Год'
final_sum_label = "final_sum"

# Настройки
input_file = 'data.xlsx'
output_path = 'output.png'
year = 2021

# Визуальное
fill_color = 'green'
edge_width = 5


def generate_graph(rows: Generator, optimal_nodes: List) -> None:
    graph = pydot.Dot(graph_type="graph", rankdir="BT")
    node_shape = "circle"
    
    _, row = next(rows)
    graph.add_node(
        pydot.Node(
            int(row[node_num_label]), 
            label=f"№{int(row[node_num_label])}\nСумма: {row['Сумма']}", 
            shape=node_shape,
            fillcolor=fill_color,
            color=fill_color,
            style="filled"
        )
    )
    
    for _, row in rows:
        node = pydot.Node(
            int(row[node_num_label]), 
            label=f"№{int(row[node_num_label])}\nСумма: {row['Сумма']}", 
            shape=node_shape,
        )
        edge = pydot.Edge(
            int(row[node_num_label]), 
            int(row[parent_label]), 
            label=row[probability_label],
        )
        
        if row[node_num_label] in optimal_nodes:
            node.set_style("filled")
            node.set_fillcolor(fill_color)
            node.set_color(fill_color)
            if row[parent_label] in optimal_nodes:
                edge.set_color(fill_color)
                edge.set_penwidth(edge_width)
            
        graph.add_node(node)
        graph.add_edge(edge)
        
    graph.write(output_path, format="png")
 
   
def get_optimal_path(data: pd.DataFrame, required_year: str) -> List:
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
        
    return nodes_in_path


def main():
    data = pd.read_excel(input_file)
    generate_graph(data.iterrows(), get_optimal_path(data, year))


if __name__ == "__main__":
    main()