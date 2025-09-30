import pandas as pd, pulp, itertools


sheet1 = pd.read_excel(r'C:\Users\Natalia Rouska\ECE\semester-8\Grammikh_Beltistopoihsh\project\dietfull.xlsx', sheet_name='Sheet1', nrows=64)
sheet2 = pd.read_excel(r'C:\Users\Natalia Rouska\ECE\semester-8\Grammikh_Beltistopoihsh\project\dietfull.xlsx', sheet_name='Sheet2')

costs = sheet1['Price/ Serving New'].tolist()
foods = sheet1['Foods'].tolist() 

Nmin = [int(x) for x in sheet2.iloc[0, 1:].tolist()] ##daily minimum intake of each nutrient
Nmax = [int(x) for x in sheet2.iloc[1, 1:].tolist()] ##daily maximum intake of each nutrient

## A[n][i] gives the amount of nutrient n in food i
A = [sheet1[col].tolist() for col in ['Calories',
     'Carbohydrates g', 'Protein g', "Dietary_Fiber g",
     'Vit_A IU', 'Vit_C IU', 'Calcium mg','Iron mg']]

M = len(foods)          # number of foods 64
N = len(A)              # number of nutrients 8
S = 2                   # maximum daily servings of each food
k = 8                   # at least 8 foods changed between days
days = []
max_iterations = 7

used_combinations = []

for run in range(max_iterations):
    prob = pulp.LpProblem(f"diet_day{run}", pulp.LpMinimize)

    x = pulp.LpVariable.dicts('x', range(M), lowBound=0,  cat=pulp.LpInteger) ##number of servings in each food
    y = pulp.LpVariable.dicts('y', range(M), cat=pulp.LpBinary) ##1 if food is chosen else 0 

    prob += pulp.lpSum([costs[i] * x[i]  for i in range(M)])

    # Nutrition Constraints
    for i in range(N):
        prob += pulp.lpSum([A[i][j] * x[j] for j in range(M)]) >= Nmin[i], f'min_nutrient_{i}'
        prob += pulp.lpSum([A[i][j] * x[j] for j in range(M)]) <= Nmax[i], f'max_nutrient_{i}'

    
    for i in range(M):
        prob += x[i] <= S * y[i], f'link_upper_{i}' ##if y[i]=0 then x[i]=0 if y[i]=1 x[i]<=S
        prob += x[i] >= y[i], f'link_lower_{i}' ## if y[i]=1 then x[i]>=1

    # exclude previous combinations for diversity
    for combo in used_combinations:
        prob += pulp.lpSum([y[i] for i in combo]) <= len(combo) - k #at least k foods changed

    # Solve
    prob.solve()

    if pulp.LpStatus[prob.status] != 'Optimal':
        print(f"Run {run}: No feasible solution found.")
        break

    chosen =[]
    chosen_foods =[]
    # if yi = 1 save combination of foods
    for v in prob.variables():
        if v.varValue == 1 and v.name.split('_')[0]=='y':
            index= int(v.name.split('_')[1])
            chosen.append(index)
        
    for v in prob.variables():
        index = int(v.name.split('_')[1])
        if index in chosen and v.name.split('_')[0]=='x' :
            chosen_foods.append([foods[index],v.varValue])

    used_combinations.append(chosen)

    solution = {
        'run': run + 1,
        'total_cost': pulp.value(prob.objective),
        'chosen_y': [int(pulp.value(y[i])) for i in range(M)], 
        'foods': chosen_foods
    }
    days.append(solution)

for sol in days:
    print(f"\n---Day #{sol['run']} ---")
    print(f"Total Cost: €{sol['total_cost']:.2f}")
    print(f"Active foods (indices): {[i for i, val in enumerate(sol['chosen_y']) if val==1]}")
    for name, servings in sol['foods']:
        print(f"  {name}: {servings:.2f} servings")

   
for (day1, sol1), (day2, sol2) in itertools.combinations(enumerate(days, start=1), 2):
    set1 = set(i for i, val in enumerate(sol1['chosen_y']) if val == 1)
    set2 = set(i for i, val in enumerate(sol2['chosen_y']) if val == 1)

    common = set1 & set2  
   

    print(f"Day {day1} vs Day {day2}:")
    print(f"Common foods ({len(common)}): {[foods[i] for i in common]}")

day_dict = {}
for sol in days:
    foods_str = "\n".join([f"{name} ({servings:.0f})" for name, servings in sol['foods']])
    day_dict[f"Day {sol['run']}"] = [f"Κόστος: €{sol['total_cost']:.2f}", foods_str]

df_summary = pd.DataFrame(day_dict, index=["Κόστος", "Μερίδες"])

