# A company that produces two types of products: chairs and tables.
# The company has constraints on the availability of labor hours, wood, and steel.
# The goal is to maximize the profit by determining the number of chairs and tables to produce

#            time            wood                    steel
# Chairs:    2 hours         4 units of wood         1 unit of steel.
# Tables:    3 hours         6 units of wood         3 units of steel.

# The profit is $5 per chair and $8 per table.

import pulp
import tkinter as tk
from tkinter import messagebox


def solve_production_plan():
    problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

    chairs = pulp.LpVariable("Chairs", lowBound=0, cat="Integer")
    tables = pulp.LpVariable("Tables", lowBound=0, cat="Integer")

    try:
        chair_profit = int(chair_profit_entry.get())
        table_profit = int(table_profit_entry.get())
        labor_hours_available = int(labor_entry.get())
        wood_available = int(wood_entry.get())
        steel_available = int(steel_entry.get())
    except:
        messagebox.showerror("Error", f"An error occurred: Invalid entry provided :(")

    profit_per_chair = chair_profit
    profit_per_table = table_profit
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


# GUI setup
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
