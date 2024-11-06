import ast


def load_code(path_to_file:str) -> ast.AST:
    #filename = 
    with open(path_to_file) as f:
        tree = ast.parse(f.read(), filename=path_to_file, mode='exec')

    return tree


def analyse_calls(tree, should_print=False) -> dict:
    calls = dict()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            call = node.func
            while True:
                if isinstance(call, ast.Attribute):
                    if type(call.value) == ast.Name and call.attr != None and len(call.attr) > 0:
                        call = f"{call.value.id}.{call.attr}"
                        break
                    call = call.value
                elif isinstance(call, ast.Call):
                    call = call.func
                elif isinstance(call, ast.Name):
                    call = call.id
                    break

            if call in calls.keys():
                calls[call] += 1
            else:
                calls[call] = 1

    if should_print:
        ordered_calls = sorted(calls.items(), key=lambda x: x[1], reverse=True)
        print("-------------------------------------")
        print("--------  Analysis of Calls  --------")
        print("-------------------------------------")
        print(f"There are {sum(calls.values())} calls.\n")
        for i, x in enumerate(ordered_calls):
            print(f"{x[1]}x {x[0]}")    # {i+1:02d}
        print("")

    return calls


def analyse_imports(tree, should_print=False) -> list:
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                imports += [f"{name.name}"]
        elif isinstance(node, ast.ImportFrom):
            for name in node.names:
                imports += [f"{node.module}.{name.name}"]

    if should_print:
        ordered_imports = sorted(imports, key=lambda x: x, reverse=False)
        print("-------------------------------------")
        print("-------  Analysis of Imports  -------")
        print("-------------------------------------")
        for i, x in enumerate(ordered_imports):
            print(f"- {x}")
        print("")

    return imports


def analyse_definitions(tree, should_print=False) -> None:
    defs = []
    lambdas = 0
    classes = []
    returns = 0
    yields = 0
    globals = 0
    nonlocals = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            defs += [node.name]
        elif isinstance(node, ast.Lambda):
            lambdas += 1
        elif isinstance(node, ast.ClassDef):
            classes += [node.name]
        elif isinstance(node, ast.Return):
            returns += 1
        elif isinstance(node, ast.Yield):
            yields += 1
        elif isinstance(node, ast.Global):
            globals += 1
        elif isinstance(node, ast.Nonlocal):
            nonlocals += 1

    if should_print:
        print("-------------------------------------")
        print("-----  Analysis of Definitions  -----")
        print("-------------------------------------")
        print(f"- Defined Functions ({len(defs)}):")
        for x in defs:
            print(f"    - {x}")
        print(f"\n- Defined Classes ({len(classes)}):")
        for x in classes:
            print(f"    - {x}")
        print(f"\n- Lambda Functions: {lambdas}")
        print(f"\n- Returns: {returns}")
        print(f"\n- Yields: {yields}")
        print(f"\n- global Keywords: {globals}")
        print(f"\n- nonlocal Keywords: {nonlocals}")
        print("")

    return None


# Control Flow
def analyse_structures(tree, should_print=False) -> None:
    ifs = 0
    fors = 0
    whiles = 0
    breaks = 0
    continues = 0
    tries = 0
    withs = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            ifs += 1
        elif isinstance(node, ast.For):
            fors += 1
        elif isinstance(node, ast.While):
            whiles += 1
        elif isinstance(node, ast.Break):
            breaks += 1
        elif isinstance(node, ast.Continue):
            continues += 1
        elif isinstance(node, ast.Try):
            tries += 1
        elif isinstance(node, ast.With):
            withs += 1

    if should_print:
        print("-------------------------------------")
        print("-----  Analysis of Structures  ------")
        print("-------------------------------------")
        print(f"- Defined loops ({fors+whiles}):")
        print(f"    - For-Loops: {fors}")
        print(f"    - While-Loops: {whiles}")
        print(f"\n- Break's: {breaks}")
        print(f"\n- Continue's: {continues}")
        print(f"\n- If-Statements: {ifs}")
        print(f"\n- Try-Blocks: {tries}")
        print(f"\n- With-Blocks: {withs}")
        print("")

    return None


def analyse_operations(tree, should_print=False) -> list:
    operations = 0
    adds = 0
    subs = 0
    mults = 0
    divs = 0
    mods = 0
    floor_divs = 0
    pows = 0

    bool_operations = 0
    ands = 0
    ors = 0
    equals = 0
    not_equals = 0
    is_ = 0
    is_not = 0
    ins = 0
    not_ins = 0
    
    for node in ast.walk(tree):

        if isinstance(node, ast.BinOp):
            operations += 1
        elif isinstance(node, ast.BoolOp) or isinstance(node, ast.Compare):
            bool_operations += 1

        # OP's
        if isinstance(node, ast.Add):
            adds += 1
        elif isinstance(node, ast.Sub):
            subs += 1
        elif isinstance(node, ast.Mult):
            mults += 1
        elif isinstance(node, ast.Div):
            divs += 1
        elif isinstance(node, ast.Mod):
            mods += 1
        elif isinstance(node, ast.FloorDiv):
            floor_divs += 1
        elif isinstance(node, ast.Pow):
            pows += 1
        # OP-BOOL's
        elif isinstance(node, ast.And):
            ands += 1
        elif isinstance(node, ast.Or):
            ors += 1
        elif isinstance(node, ast.Eq):
            equals += 1
        elif isinstance(node, ast.NotEq):
            not_equals += 1
        elif isinstance(node, ast.Is):
            is_ += 1
        elif isinstance(node, ast.IsNot):
            is_not += 1
        elif isinstance(node, ast.In):
            ins += 1
        elif isinstance(node, ast.NotIn):
            not_ins += 1

    if should_print:
        print("-------------------------------------")
        print("-----  Analysis of Operations  ------")
        print("-------------------------------------")
        print(f"- Operations ({operations}):")
        print(f"    - Add's: {adds}")
        print(f"    - Sub's: {subs}")
        print(f"    - Mult's: {mults}")
        print(f"    - Div's: {divs}")
        print(f"    - Mod's: {mods}")
        print(f"    - Floor Div's: {floor_divs}")
        print(f"    - Pow's: {pows}")
        print(f"\n- Bool Operations ({bool_operations}):")
        print(f"    - And's: {ands}")
        print(f"    - Or's: {ors}")
        print(f"    - Equals's: {equals}")
        print(f"    - Not Equals's: {not_equals}")
        print(f"    - Is's: {is_}")
        print(f"    - Is not's: {is_not}")
        print(f"    - In's: {ins}")
        print(f"    - Not In's: {not_ins}")
        print("")

    return [('Add', adds), ('Sub', subs), ('Mult', mults), ('Div', divs), ('Mod', mods), ('Floor Div', floor_divs), ('Pow', pows), 
            ('And', ands), ('Or', ors), ('Equal', equals), ('Not Equal', not_equals), ('Is', is_), ('Is Not', is_not), ('In', ins), ('Not In', not_ins)]


def visualize(calls:dict, imports:list, ops:list):
    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots(2, 1, figsize=(20, 10))
    
    x = []
    y = []
    counter = 0
    for name, value in sorted(calls.items(), key=lambda x: x[1], reverse=True):
        if counter >= 10:
            break
        x += [name]
        y += [value]
        counter += 1

    ax[0].set_title("Popular Function-Calls")
    ax[0].bar(x, y, align='center', width=0.5)

    x = []
    y = []
    for name, value in ops:
        x += [name]
        y += [value]
    ax[1].set_title("Operations")
    ax[1].bar(x, y)

    plt.show()


def analyse_code(path_to_file:str, should_print=False, should_visualize=False):
    # Analysis
    if should_print:
        title = f"    >>> Analysis of {path_to_file.split('/')[-1]} <<<    "
        print("_"*len(title))
        print(f"{title}\n")
    tree = load_code(path_to_file)
    calls = analyse_calls(tree, should_print)
    imports = analyse_imports(tree, should_print)
    analyse_definitions(tree, should_print)
    analyse_structures(tree, should_print)
    operations = analyse_operations(tree, should_print)
    if should_print:
        print(f"\n{' '*(len(title)//2-11)}>>> END of Analysis <<<")
        print("_"*len(title))

    # Visualisation
    if should_visualize:
        visualize(calls, imports, operations)


