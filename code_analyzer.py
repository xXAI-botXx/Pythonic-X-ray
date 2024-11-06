import os
import ast
import matplotlib.pyplot as plt


def load_code(path_to_file:str) -> ast.AST:
     
    with open(path_to_file) as f:
        tree = ast.parse(f.read(), filename=path_to_file, mode='exec')

    return tree


def analyse_calls(tree) -> dict:
    calls = dict()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            call = node.func
            call_name = None
            
            while call:
                if isinstance(call, ast.Attribute):
                    if isinstance(call.value, ast.Name) and call.attr:
                        call_name = f"{call.value.id}.{call.attr}"
                        break
                    call = call.value
                elif isinstance(call, ast.Call):
                    call = call.func
                elif isinstance(call, ast.Name):
                    call_name = call.id
                    break
                else:
                    break
            
            if call_name:
                calls[call_name] = calls.get(call_name, 0) + 1

    return calls


def analyse_imports(tree) -> list:
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                imports += [f"{name.name}"]
        elif isinstance(node, ast.ImportFrom):
            for name in node.names:
                imports += [f"{node.module}.{name.name}"]

    return imports


def analyse_definitions(tree) -> None:
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

    return defs, lambdas, classes, returns, yields, globals, nonlocals


# Control Flow
def analyse_structures(tree) -> None:
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

    return ifs, fors, whiles, breaks, continues, tries, withs


def analyse_operations(tree) -> list:
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

    # return [('Add', adds), ('Sub', subs), ('Mult', mults), ('Div', divs), ('Mod', mods), ('Floor Div', floor_divs), ('Pow', pows), 
    #        ('And', ands), ('Or', ors), ('Equal', equals), ('Not Equal', not_equals), ('Is', is_), ('Is Not', is_not), ('In', ins), ('Not In', not_ins)]

    return operations, adds, subs, mults, divs, mods, floor_divs, pows, bool_operations, ands, ors, equals, not_equals, is_, is_not, ins, not_ins


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


def create_analysis_str(
        name,
        calls,
        imports,
        definitions,
        structures,
        operations
        ):
    
    # begin
    title = f"\n    >>> Analysis of {name} <<<    \n"
    title_len = len(title)
    analylsis = f"\n\n{'_'*title_len}"
    analylsis += title

    # call
    ordered_calls = sorted(calls.items(), key=lambda x: x[1], reverse=True)
    analylsis += "\n-------------------------------------"
    analylsis += "\n--------  Analysis of Calls  --------"
    analylsis += "\n-------------------------------------"
    analylsis += f"\nThere are {sum(calls.values())} calls.\n"
    for i, x in enumerate(ordered_calls):
        analylsis += f"\n{x[1]}x {x[0]}"    # {i+1:02d}
    analylsis += "\n"

    # imports
    ordered_imports = sorted(imports, key=lambda x: x, reverse=False)
    analylsis += "\n-------------------------------------"
    analylsis += "\n-------  Analysis of Imports  -------"
    analylsis += "\n-------------------------------------"
    for i, x in enumerate(ordered_imports):
        analylsis += f"\n- {x}"
    analylsis += "\n"

    # definitions
    defs, lambdas, classes, returns, yields, globals, nonlocals = definitions
    analylsis += "\n-------------------------------------"
    analylsis += "\n-----  Analysis of Definitions  -----"
    analylsis += "\n-------------------------------------"
    analylsis += f"\n- Defined Functions ({len(defs)}):"
    for x in defs:
        analylsis += f"\n    - {x}"
    analylsis += f"\n\n- Defined Classes ({len(classes)}):"
    for x in classes:
        analylsis += f"\n    - {x}"
    analylsis += f"\n\n- Lambda Functions: {lambdas}"
    analylsis += f"\n\n- Returns: {returns}"
    analylsis += f"\n\n- Yields: {yields}"
    analylsis += f"\n\n- global Keywords: {globals}"
    analylsis += f"\n\n- nonlocal Keywords: {nonlocals}"
    analylsis += "\n"

    # structures
    ifs, fors, whiles, breaks, continues, tries, withs = structures
    analylsis += "\n-------------------------------------"
    analylsis += "\n-----  Analysis of Structures  ------"
    analylsis += "\n-------------------------------------"
    analylsis += f"\n- Defined loops ({fors+whiles}):"
    analylsis += f"\n    - For-Loops: {fors}"
    analylsis += f"\n    - While-Loops: {whiles}"
    analylsis += f"\n\n- Break's: {breaks}"
    analylsis += f"\n\n- Continue's: {continues}"
    analylsis += f"\n\n- If-Statements: {ifs}"
    analylsis += f"\n\n- Try-Blocks: {tries}"
    analylsis += f"\n\n- With-Blocks: {withs}"
    analylsis += "\n"

    # operations
    operations, adds, subs, mults, divs, mods, floor_divs, pows, bool_operations, ands, ors, equals, not_equals, is_, is_not, ins, not_ins = operations
    analylsis += "\n-------------------------------------"
    analylsis += "\n-----  Analysis of Operations  ------"
    analylsis += "\n-------------------------------------"
    analylsis += f"\n- Operations ({operations}):"
    analylsis += f"\n    - Add's: {adds}"
    analylsis += f"\n    - Sub's: {subs}"
    analylsis += f"\n    - Mult's: {mults}"
    analylsis += f"\n    - Div's: {divs}"
    analylsis += f"\n    - Mod's: {mods}"
    analylsis += f"\n    - Floor Div's: {floor_divs}"
    analylsis += f"\n    - Pow's: {pows}"
    analylsis += f"\n\n- Bool Operations ({bool_operations}):"
    analylsis += f"\n    - And's: {ands}"
    analylsis += f"\n    - Or's: {ors}"
    analylsis += f"\n    - Equals's: {equals}"
    analylsis += f"\n    - Not Equals's: {not_equals}"
    analylsis += f"\n    - Is's: {is_}"
    analylsis += f"\n    - Is not's: {is_not}"
    analylsis += f"\n    - In's: {ins}"
    analylsis += f"\n    - Not In's: {not_ins}"
    analylsis += "\n"

    # end
    analylsis += f"\n{' '*(title_len//2-11)}>>> END of Analysis <<<\n"
    analylsis += "_"*title_len

    return analylsis


# def add_new_entry(
#                 calls
#                 imports
#                 definitions
#                 structures
#                 operations
#                 )


def analyse_code(path_to_file_or_dir:str, name:str, save_path:str, should_print=True, should_save=True):    #should_visualize=False):
    # Analysis
    if os.path.isdir(path_to_file_or_dir):
        pass
        # empty init
        ...

        # analyse every py file
        for cur_root, cur_dirs, cur_files in os.path.walk(path_to_file_or_dir):
            for cur_file in cur_files:
                if cur_file.endswith(".py"):   # or cur_file.endswith(".ipynb"):
                    tree = load_code(os.path.join(cur_root, cur_file))
                    calls = analyse_calls(tree)
                    imports = analyse_imports(tree)
                    analyse_definitions(tree)
                    analyse_structures(tree)
                    operations = analyse_operations(tree)

                    # merge
                    # ...
    else:
        tree = load_code(path_to_file_or_dir)
        calls = analyse_calls(tree)
        imports = analyse_imports(tree)
        definitions = analyse_definitions(tree)
        structures = analyse_structures(tree)
        operations = analyse_operations(tree)


    analysis_str = create_analysis_str(name=name, calls=calls, imports=imports, definitions=definitions, structures=structures, operations=operations)

    if should_print:
        print(analysis_str)

    if should_save:
        with open(os.path.join(save_path, "code_analysis.txt"), "w") as file:
            file.write(analysis_str)

    # Visualisation
    # if should_visualize:
    #     visualize(calls, imports, operations)


