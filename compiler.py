

__CompilerVersions__ = ["0.1.0"]
__ScratchOSCompilerVersions__ = {"0.9.5":"0.1.0","0.10.4":"0.1.0"}
__ScratchOSVersion__ = "0.10.4"
__Compiler__ = "0.1.0"
__VariablePrefixCharecters__ = {"0.1.0":"$"}


def CollectVariableNames(code,varPrefix = '$'):
    variable_names = []
    for word in code.split():
        if (word[0]) == '$':
            variable_names.append(word)
    return variable_names

def AssignVariableValues(variable_names):
    variable_ids = {}
    current_adress = 1
    for variable_name in variable_names:
        if variable_name in variable_ids:
            continue
        print(variable_ids)
        adress = str(current_adress)
        while len(adress) < 4:
            adress = "0"+adress
        variable_ids[variable_name] = adress
        current_adress += 1
    return variable_ids
        
def SubstituteVariables(code,variable_ids):
    lines = []
    words = []
    for line in code.split('\n'):
        words = []
        for word in line.split():
            if word in variable_ids:
                print(variable_ids)
                words.append(str(variable_ids[word]))
            else:
                words.append(word)
        lines.append(" ".join(words))
    return "\n".join(lines)

def Compile(code,CompilerVersion = None,ScratchOSVersion = None):
    if ScratchOSVersion != None and CompilerVersion == None:
        CompilerVersion = __ScratchOSCompilerVersions__[ScratchOSVersion]
    if CompilerVersion == None:
        CompilerVersion = __Compiler__
    print(CompilerVersion in ["0.1.0"])
    if CompilerVersion in ["0.1.0"]:
        return __Compile_0_1_0__(code)
        
def __Compile_0_1_0__(code):
    variable_names = CollectVariableNames(code)
    variable_ids = AssignVariableValues(variable_names)
    code = SubstituteVariables(code,variable_ids)
    print(code)
    return code
        