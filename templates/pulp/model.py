
import pulp, inspect

from libs import Log, Timed

time_limit = 10

n = 10
capacity = 165

index = map(str, range(n))
weights =  pulp.makeDict([index], [23, 31, 29, 44, 53, 38, 63, 85, 89, 82])
values =   pulp.makeDict([index], [92, 57, 49, 68, 60, 43, 67, 84, 87, 72])

lp_vars = pulp.LpVariable.dicts("x", index, 0, 1, pulp.LpInteger)
prob = pulp.LpProblem("Knapsack Problem", sense=pulp.LpMaximize)

prob += pulp.lpSum([lp_vars[i] * values[i] for i in index]), "Total_Value"

prob += pulp.lpSum([lp_vars[i] * weights[i] for i in index]) <= capacity, "Capacity"

prob.solve()

Log.info(pulp.LpStatus[prob.status])
Log.info(pulp.value(prob.objective))
for v in prob.variables():
  Log(v.name + ' = ' + str(v.varValue))
