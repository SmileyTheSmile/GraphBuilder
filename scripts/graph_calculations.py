import pydot
import pandas as pd

from typing import Generator, List, Tuple
from sqlalchemy import create_engine
from PIL import Image

if __name__ != "__main__":
    import scripts.settings as set
else:
    import settings as set


class Control:
    def __init__(self):
        self.data = None
        self.engine = None
        self.engine = None
        self.optimal_nodes = []
        
    def connect_to_db(
        self,
        login: str,
        password: str,
        database: str,
        server: str,
        port: str,
        ):
        self.engine = create_engine(f'postgresql:///?user={login}&password={password}&database={database}&host={server}&port={port}')
    
    def get_data_db(self):
        self.data = pd.read_sql(
            sql='''
                    SELECT id, id_parent, earnings, probability, year 
                    FROM earnings_predictions 
                ''', 
            con=self.engine,
        )
            
    def get_data_csv(self):
        self.data = pd.read_excel(set.input_file)
        return self.data, self.get_optimal_path(set.data, )
            
    def generate_graphs(self) -> None:
        rows = self.data.iterrows()
        
        graph = pydot.Dot(graph_type="graph", rankdir="BT")
        cooler_graph = pydot.Dot(graph_type="graph", rankdir="BT")
        
        _, row = next(rows)
        graph.add_node(
            pydot.Node(
                int(row[set.id_row]), 
                label=f"№{int(row[set.id_row])}\nСумма: {row[set.earnings_row]}", 
                shape=set.node_shape,
            )
        )
        cooler_graph.add_node(
            pydot.Node(
                int(row[set.id_row]), 
                label=f"№{int(row[set.id_row])}\nСумма: {row[set.final_sum_row]}", 
                shape=set.node_shape,
                fillcolor=set.fill_color,
                color=set.fill_color,
                style="filled"
            )
        )
        
        for _, row in rows:
            row_sum = row[set.earnings_row]
            row_node_num = int(row[set.id_row])
            row_parent = int(row[set.id_parent_row])
            
            node = pydot.Node(
                name=row_node_num, 
                label=f"№{row_node_num}\nСумма: {row_sum}", 
                shape=set.node_shape,
            )
            edge = pydot.Edge(
                src=row_node_num, 
                dst=row_parent, 
                label=row[set.probability_row],
            )
            
            cooler_node = pydot.Node(
                name=row_node_num, 
                label=f"№{row_node_num}\nСумма: {row[set.final_sum_row]}", 
                shape=set.node_shape,
            )
            cooler_edge = pydot.Edge(
                src=row_node_num, 
                dst=row_parent, 
                label=row[set.probability_row],
            )
            
            if row[set.id_row] in self.optimal_nodes:
                cooler_node.set_style("filled")
                cooler_node.set_fillcolor(set.fill_color)
                cooler_node.set_color(set.fill_color)
                if row_parent in self.optimal_nodes:
                    cooler_edge.set_color(set.fill_color)
                    cooler_edge.set_penwidth(set.edge_width)
                
            graph.add_node(node)
            graph.add_edge(edge)
                
            cooler_graph.add_node(cooler_node)
            cooler_graph.add_edge(cooler_edge)
            
        graph.write(path=f'{set.output_path}{set.graph_raw_file_name}', format="png")
        cooler_graph.write(path=f'{set.output_path}{set.cooler_raw_graph_file_name}', format="png")
    
    def get_optimal_path(self) -> bool:
            grouped = self.data.groupby(set.year_row)

            data_by_year = {}
            years = []

            for year, group in grouped:
                years.append(year)
                data_by_year[year] = group.reset_index(drop=True)
            
            if set.year not in years:
                print("Wrong year")
                return False
            
            required_year_data = data_by_year[set.year]
            max_final_sum_in_last_year = max(required_year_data[set.final_sum_row])
            last_node_row = required_year_data[required_year_data[set.final_sum_row] == max_final_sum_in_last_year]
            
            nodes_in_path = [last_node_row[set.id_row].item()]
            parent = last_node_row[set.id_parent_row]
            
            while not parent.isna().all():
                current_row = self.data[self.data[set.id_row] == parent.item()]
                nodes_in_path.append(current_row[set.id_row].item())
                parent = current_row[set.id_parent_row]
                
            self.optimal_nodes = nodes_in_path
            
            return True

    def resize_graphs() -> None:
        img = Image.open(f'{set.output_path}{set.graph_raw_file_name}')
        img = img.resize((int(img.size[0] / 2), int(img.size[1] / 2)), Image.Resampling.LANCZOS)
        img.save(f'{set.output_path}{set.graph_file_name}')
        
        img = Image.open(f'{set.output_path}{set.cooler_raw_graph_file_name}')
        img = img.resize((int(img.size[0] / 2), int(img.size[1] / 2)), Image.Resampling.LANCZOS)
        img.save(f'{set.output_path}{set.cooler_graph_file_name}')

