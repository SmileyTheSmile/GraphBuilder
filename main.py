import graph_calculations as gc
import settings


def main():
    gc.generate_graph(*gc.get_optimal_path(settings.input_file, settings.year))


if __name__ == "__main__":
    main()