import pulp
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from tkinter import messagebox


def solve_production_plan():
    problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

    chairs = pulp.LpVariable("Chairs", lowBound=0, cat="Integer")
    tables = pulp.LpVariable("Tables", lowBound=0, cat="Integer")

    try:
        profit_per_chair = int(chair_profit_entry.get())
        profit_per_table = int(table_profit_entry.get())
        labor_hours_available = int(labor_entry.get())
        wood_available = int(wood_entry.get())
        steel_available = int(steel_entry.get())
    except:
        messagebox.showerror("Error", f"An error occurred: Invalid entry provided :(")
        return

    problem += profit_per_chair * chairs + profit_per_table * tables

    problem += 2 * chairs + 3 * tables <= labor_hours_available
    problem += 4 * chairs + 6 * tables <= wood_available
    problem += chairs + 3 * tables <= steel_available

    problem.solve()
    optimal_chairs = pulp.value(chairs)
    optimal_tables = pulp.value(tables)
    total_profit = pulp.value(problem.objective)

    result_label.config(
        text=f"Number of chairs = {optimal_chairs}\nNumber of tables = {optimal_tables}\nTotal profit = ${total_profit}"
    )

    plot_feasible_region(
        labor_hours_available, wood_available, steel_available
    )  # our plot after solving the ploblem


############################################################################################################################# PLOT #
def plot_feasible_region(labor_hours_available, wood_available, steel_available):
    def labor_constraint(chairs):
        return (labor_hours_available - 2 * chairs) / 3

    def wood_constraint(chairs):
        return (wood_available - 4 * chairs) / 6

    def steel_constraint(chairs):
        return steel_available - chairs / 1

    chairs_vals = np.linspace(0, max(labor_hours_available // 2, wood_available // 4, steel_available), 100)

    labor_tables = labor_constraint(chairs_vals)
    wood_tables = wood_constraint(chairs_vals)
    steel_tables = steel_constraint(chairs_vals)

    plt.figure(figsize=(8, 6))
    plt.plot(
        chairs_vals,
        labor_tables,
        label="Labor Constraint: 2*chairs + 3*tables <= labor_hours",
    )
    plt.plot(chairs_vals, wood_tables, label="Wood Constraint: 4*chairs + 6*tables <= wood")
    plt.plot(chairs_vals, steel_tables, label="Steel Constraint: chairs + 3*tables <= steel")

    plt.fill_between(
        chairs_vals,
        0,
        np.minimum.reduce([labor_tables, wood_tables, steel_tables]),
        alpha=0.2,
        label="Feasible Region",
        color="gray",
    )

    plt.xlabel("Chairs")
    plt.ylabel("Tables")
    plt.title("Feasible Region")
    plt.legend()
    plt.grid()
    plt.show()


############################################################################################################################## GUI #
root = tk.Tk()
root.title("Production Planning Solver")

input_frame = tk.Frame(root)
input_frame.pack(padx=20, pady=20)

chair_profit_label = tk.Label(input_frame, text="Chair Profit:")
chair_profit_label.grid(row=0, column=0)
chair_profit_entry = tk.Entry(input_frame)
chair_profit_entry.grid(row=0, column=1)

table_profit_label = tk.Label(input_frame, text="Table Profit:")
table_profit_label.grid(row=1, column=0)
table_profit_entry = tk.Entry(input_frame)
table_profit_entry.grid(row=1, column=1)

labor_label = tk.Label(input_frame, text="Labor Hours Available:")
labor_label.grid(row=2, column=0)
labor_entry = tk.Entry(input_frame)
labor_entry.grid(row=2, column=1)

wood_label = tk.Label(input_frame, text="Wood Available:")
wood_label.grid(row=3, column=0)
wood_entry = tk.Entry(input_frame)
wood_entry.grid(row=3, column=1)

steel_label = tk.Label(input_frame, text="Steel Available:")
steel_label.grid(row=4, column=0)
steel_entry = tk.Entry(input_frame)
steel_entry.grid(row=4, column=1)

solve_button = tk.Button(root, text="Solve", command=solve_production_plan)
solve_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
