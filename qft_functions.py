import re
import os
import wolfram_utils as wu

def count_elements(s: str):
    # Find all contents inside { ... }
    contents = re.findall(r'\{([^}]*)\}', s)
    counts = []
    for c in contents:
        # Remove extra spaces and split by comma
        items = [item.strip() for item in c.split(',') if item.strip()]
        counts.append(len(items))
    
    # If the string has exactly two groups (e.g. A -> B), return a tuple
    if len(counts) == 2:
        return counts[0], counts[1]
    return tuple(counts)

def feynarts_create_amp(process: str, order: int, model: str = "QED"):
    in_num, out_num = count_elements(process)
    code = f"""
If[$FrontEnd === Null, $InputFileName, NotebookFileName[]] // DirectoryName // SetDirectory;
Get["FeynArts`"];
top = CreateTopologies[{order}, Length/@({process}), ExcludeTopologies -> {{Tadpoles, WFCorrections}}];
diags = InsertFields[top, {process}, Model -> "{model}", InsertionLevel -> {{Particles}}];
amp = CreateFeynAmp[diags, Truncated -> True, PreFactor -> 1];
Put[amp, "amp"];
Quit[];
"""
    wu.create_wolfram_script("", "feynarts_create_amp.wl", code)
    wu.run_wolfram_script_simple("feynarts_create_amp.wl")
    return os.getcwd() + "/amp"

def calcloop_amplitude_squared(amp_file1: str, amp_file2 = 1):
    if amp_file2 is str:
        amp_file2 = f"\"\{amp_file2}\""

    code = f"""
If[$FrontEnd === Null, $InputFileName, NotebookFileName[]] // DirectoryName // SetDirectory;
Get["/home/huang/Downloads/MCPtest-main/calcloop-main/CalcLoop.wl"];
SetOptions[FeynArtsReadAmp, "ExternalMomentumName" -> (Symbol["p" <> ToString@#] &)];
AmplitudeSquared["ampSq", "{amp_file1}", {amp_file2}];
Put[Get["ampSq/AmplitudeSquared"]/.{{CalcLoopSymbol:>Symbol,$D->4-2eps}},"ampSq/AmplitudeSquared"];
Quit[];
"""
    wu.create_wolfram_script("", "calcloop_amplitude_squared.wl", code)
    wu.run_wolfram_script_simple("calcloop_amplitude_squared.wl")
    return os.getcwd() + "/ampSq/AmplitudeSquared"

def calcloop_family_decomposition(ampSq_file: str):
    code = f"""
If[$FrontEnd === Null, $InputFileName, NotebookFileName[]] // DirectoryName // SetDirectory;
Get["/home/huang/Downloads/MCPtest-main/calcloop-main/CalcLoop.wl"];
FamilyDecomposition["family", "{ampSq_file}"];
Quit[];
"""
    wu.create_wolfram_script("", "calcloop_family_decomposition.wl", code)
    wu.run_wolfram_script_simple("calcloop_family_decomposition.wl")
    return os.getcwd() + "/family/Families"

def calcloop_amflow_calculate_FI(family_file: str, numeric: str = "{}"):
    code = f"""
If[$FrontEnd === Null, $InputFileName, NotebookFileName[]] // DirectoryName // SetDirectory;
Get["/home/huang/Downloads/MCPtest-main/calcloop-main/CalcLoop.wl"];
SetOptions[AMFlowCalculateFI, "Numeric"->{numeric}];
res = AMFlowCalculateFI["CalcFI", "{family_file}"]/.x_String :> ToExpression[x]/. CalcLoopSymbol[x__] :> x;
Put[res, "res"];
Quit[];
"""
    wu.create_wolfram_script("", "calcloop_amflow_calculate_FI.wl", code)
    wu.run_wolfram_script_simple("calcloop_amflow_calculate_FI.wl")
    return os.getcwd() + "/res"

if __name__ == "__main__":
    file = feynarts_create_amp("{F[1,1]} -> {F[1,1]}", 1)
    file = calcloop_amplitude_squared(file)
    file = calcloop_family_decomposition(file)
    file = calcloop_amflow_calculate_FI(file,"{ME->1,MM->1,ML->1}")
    print(file)
    
