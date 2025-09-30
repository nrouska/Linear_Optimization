import pandas as pd
import pulp

sheet1 = pd.read_excel(r'C:\Users\Natalia Rouska\ECE\semester-8\Grammikh_Beltistopoihsh\project\dietfull.xlsx', sheet_name='Sheet1', nrows=64)
sheet2 = pd.read_excel(r'C:\Users\Natalia Rouska\ECE\semester-8\Grammikh_Beltistopoihsh\project\dietfull.xlsx', sheet_name='Sheet2')

costs = sheet1['Price/ Serving New'].tolist()
foods = sheet1['Foods'].tolist()
print(foods)
Nmin = [int(x) for x in sheet2.iloc[0, 1:].tolist()] ##daily minimum intake of each nutrient
Nmax = [int(x) for x in sheet2.iloc[1, 1:].tolist()] ##daily maximum intake of each nutrient

## A[n][i] gives the amount of nutrient n in food i
A = [sheet1[col].tolist() for col in ['Calories',
     'Carbohydrates g', 'Protein g', "Dietary_Fiber g",
     'Vit_A IU', 'Vit_C IU', 'Calcium mg','Iron mg']]



M = len(foods)          # number of foods
D = list(range(3))      # 3 days plan
N = len(A)              # number of nutrients
S = 3                  # maximum daily servings of each food

prob = pulp.LpProblem("full_diet", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((foods[i], d) for i in range(M) for d in D), lowBound=0,upBound=S, cat='Continuous') #servings of food i in day d
y = pulp.LpVariable.dicts("y", ((foods[i], d) for i in range(M) for d in D), cat='Binary')  #indicating if food i in day d is selected

# minimmize cost 
prob += pulp.lpSum(costs[i] * x[(foods[i], d)] for i in range(M) for d in D)

# Nutrition constraints 
##for each nutrient and each day the total nutrient intake of the foods selected must be in [Nmin[n],Nmax[n]]
for n in range(N):
    for d in D:
        prob += pulp.lpSum(A[n][i] * x[(foods[i], d)] for i in range(M)) >= Nmin[n], f"min_nutrient_{n}_day_{d}"
        prob += pulp.lpSum(A[n][i] * x[(foods[i], d)] for i in range(M)) <= Nmax[n], f"max_nutrient_{n}_day_{d}"

##if y[f,d]=1 then 1<=x[f,d]<=S
for i in range(M):
    f = foods[i]
    for d in D:
        prob += x[(f, d)] <= S * y[(f, d)], f"link_upper_{f}_{d}"
        prob += x[(f, d)] >= y[(f, d)], f"link_lower_{f}_{d}"

# variety in foods
# each food is chosen once in the plan y[i,0]+y[i,1]+...<=1
for i in range(M):
    f = foods[i]
    prob += pulp.lpSum(y[(f, d)] for d in D) <= 1

# Solve the problem
prob.solve()


print(f"Status: {pulp.LpStatus[prob.status]}")
print(f"Objective: {pulp.value(prob.objective)}")

for d in D:
    print(f"\nDay {d + 1}:")
    for i in range(M):
        f = foods[i]
        servings = x[(f, d)].varValue
        if servings > 0:
            print(f"  {f}: {servings} servings")



days_text = []
costs_text = []

for d in D:
    foods_list = []
    total_cost = 0
    for i in range(M):
        servings = x[(foods[i], d)].varValue
        if servings > 0:
            foods_list.append(f"{foods[i]}: {servings}")
            total_cost += costs[i] * servings
    days_text.append("\n".join(foods_list))
    costs_text.append(f"{total_cost:.2f} €")

df = pd.DataFrame([costs_text, days_text], index=["Total Cost", "Foods/Servings"], columns=[f"Day {d+1}" for d in D])



