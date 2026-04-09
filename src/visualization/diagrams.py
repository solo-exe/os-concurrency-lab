import os

import graphviz


def generate_architecture_diagram():
    """Generates the architecture flowchart for the synchronization simulation."""
    os.makedirs("outputs", exist_ok=True)

    dot = graphviz.Digraph(comment="Simulation Architecture", format="png")
    dot.attr(rankdir="TB", size="8,8")

    dot.node("M", "main.py\n(Entry Point)")

    # Core Engine
    dot.node("E", "SimulationEngine")
    dot.node("MT", "MetricsTracker\n(CPU, Time, Waiting)")

    # Algorithms
    with dot.subgraph(name="cluster_0") as c:
        c.attr(style="filled", color="lightgrey")
        c.node_attr.update(style="filled", color="white")
        c.node("A_Base", "SyncAlgorithm (Interface)")
        c.node("A_Dekker", "Dekker's\n(Busy-Wait)")
        c.node("A_Peter", "Peterson's\n(Busy-Wait)")
        c.node("A_Sem", "Semaphore\n(Blocking)")
        c.edge("A_Dekker", "A_Base", style="dashed")
        c.edge("A_Peter", "A_Base", style="dashed")
        c.edge("A_Sem", "A_Base", style="dashed")
        c.attr(label="Algorithms")

    # Visualizations
    dot.node("V_Chart", "charts.py\n(Matplotlib/Seaborn)")
    dot.node("V_Diag", "diagrams.py\n(Graphviz)")

    dot.edge("M", "E", label="Starts")
    dot.edge("M", "V_Chart", label="Plots data")
    dot.edge("M", "V_Diag", label="Draws flows")
    dot.edge("E", "MT", label="Records to")
    dot.edge("E", "A_Base", label="Uses")

    filepath = os.path.join("outputs", "architecture_diagram")
    try:
        dot.render(filepath, view=False)
        print(f"Saved diagram: {filepath}.png")
    except Exception as e:
        print(f"Failed to render diagram (Is graphviz installed?): {e}")


def generate_synchronization_timeline():
    """Generates a sequence diagram approximation for Dekker/Peterson vs Semaphore."""
    dot = graphviz.Digraph(comment="Sync Timeline", format="png")
    dot.attr(rankdir="LR")

    with dot.subgraph(name="cluster_1") as c:
        c.attr(label="Dekker / Peterson (Busy Wait)")
        c.node("T1_BW", "Thread 1")
        c.node("T2_BW", "Thread 2")
        c.node("CS_BW", "Critical Section")

        c.edge("T1_BW", "CS_BW", label="wants to enter")
        c.edge("T2_BW", "CS_BW", label="wants to enter (SPINS / 100% CPU)")
        c.edge("CS_BW", "T1_BW", label="leaves (turn=T2)")
        c.edge("T2_BW", "CS_BW", label="enters (stops spinning)")

    with dot.subgraph(name="cluster_2") as c:
        c.attr(label="Semaphore (Blocking)")
        c.node("T1_S", "Thread 1")
        c.node("T2_S", "Thread 2")
        c.node("OS_S", "OS Scheduler")
        c.node("CS_S", "Critical Section")

        c.edge("T1_S", "CS_S", label="acquire(1 -> 0)")
        c.edge("T2_S", "CS_S", label="acquire (Blocks / 0% CPU)")
        c.edge("T2_S", "OS_S", label="sleeps")
        c.edge("T1_S", "CS_S", label="release(0 -> 1)")
        c.edge("OS_S", "T2_S", label="wakes up")
        c.edge("T2_S", "CS_S", label="enters")

    filepath = os.path.join("outputs", "synchronization_timeline")
    try:
        dot.render(filepath, view=False)
        print(f"Saved diagram: {filepath}.png")
    except Exception as e:
        print(f"Failed to render timeline (Is graphviz installed?): {e}")
