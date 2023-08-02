import methods.methods as m
import methods.formatting as f
from results import save_results


agent, start, end, desc, graph = m.setup()

print(f.format_title(f"Start: {start}, Goal: {end}"))
print("===")

print(f.format_title("Breadth-First Search (BFS)"))
bfs_path = m.bfs(graph, start, end)
print(f.format_results(bfs_path, 50, end, "BFS Results"))
print("===")

print(f.format_title("Singular LLM"))
single_path = m.run_method("singular", agent, start, end, desc, graph)
print(f.format_results(single_path, 50, end, "Singular LLM Results"))
print("===")

print(f.format_title("Ensemble LLMs"))
ensemble_path = m.run_method("ensemble", agent, start, end, desc, graph)
print(f.format_results(ensemble_path, 50, end, "Ensemble LLMs Results"))
print("===")

print(f.format_title("Divide and Conquer LLMs"))
dc_path = m.run_method("dc", agent, start, end, desc, graph)
print(f.format_results(dc_path, 50, end, "Divide and Conquer LLMs Results"))
print("===")

print(f.format_title("Consulting LLMs"))
consult_path = m.run_method("consult", agent, start, end, desc, graph)
print(f.format_results(consult_path, 50, end, "Consulting LLMs Results"))
print("===")

print(f.format_title("Stacking LLMs"))
stack_path = m.run_method("stack", agent, start, end, desc, graph)
print(f.format_results(stack_path, 50, end, "Stacking LLMs Results"))
print("===")

save_results(start, end, bfs=bfs_path, singular=single_path,
             ensemble=ensemble_path, dc=dc_path, consult=consult_path,
             stack=stack_path)
