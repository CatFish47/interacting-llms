import methods.methods as m
import methods.formatting as f
from results import save_results

for i in range(100):
    agent, start, end, desc, graph = m.setup()
    width = 50

    print(f.format_title(f"Start: {start}, Goal: {end}"))
    print("===")

    print(f.format_title("Breadth-First Search (BFS)"))
    bfs_res = m.bfs(graph, start, end)
    print(f.format_results(bfs_res, width, end, "BFS Results"))
    print("===")

    print(f.format_title("Singular LLM"))
    single_res = m.run_method("singular", agent, start, end, desc, graph)
    print(f.format_results(single_res, width, end, "Singular LLM Results"))
    print("===")

    print(f.format_title("Ensemble LLMs"))
    ensemble_res = m.run_method("ensemble", agent, start, end, desc, graph)
    print(f.format_results(ensemble_res, width, end, "Ensemble LLMs Results"))
    print("===")

    print(f.format_title("Divide and Conquer LLMs"))
    dc_res = m.run_method("dc", agent, start, end, desc, graph)
    print(f.format_results(dc_res, width, end, "Divide and Conquer LLMs Results"))
    print("===")

    print(f.format_title("Consulting LLMs"))
    consult_res = m.run_method("consult", agent, start, end, desc, graph)
    print(f.format_results(consult_res, width, end, "Consulting LLMs Results"))
    print("===")

    print(f.format_title("Stacking LLMs"))
    stack_res = m.run_method("stack", agent, start, end, desc, graph)
    print(f.format_results(stack_res, width, end, "Stacking LLMs Results"))
    print("===")

    save_results(start, end, bfs=bfs_res, singular=single_res,
                ensemble=ensemble_res, dc=dc_res, consult=consult_res,
                stack=stack_res)
