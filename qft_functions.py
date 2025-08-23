import re
import os
import wolfram_utils as wu

def mk_process_dir(process: str, order: int):
    process_dir = f"{process}@{order}loop"
    os.makedirs(process_dir, exist_ok=True)
    return process_dir

def feynarts_create_amp(process: str, order: int, model: str = "QED", process_dir: str = "cache"):
    code = f"""
If[$FrontEnd === Null, $InputFileName, NotebookFileName[]] // DirectoryName // SetDirectory;
Get["FeynArts`"];
top = CreateTopologies[{order}, Length/@({process}), ExcludeTopologies -> {{Tadpoles, WFCorrections}}];
diags = InsertFields[top, {process}, Model -> "{model}", InsertionLevel -> {{Particles}}];
amp = CreateFeynAmp[diags, Truncated -> True, PreFactor -> 1];
Put[amp, "amp"];
Quit[];
"""
    wu.create_wolfram_script(process_dir, "feynarts_create_amp.wl", code)
    wu.run_wolfram_script_simple(process_dir + "/feynarts_create_amp.wl")
    return os.getcwd() + "/" + process_dir + "/amp"

def calcloop_amplitude_squared(amp_file1: str, amp_file2 = 1, process_dir: str = "cache"):
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
    wu.create_wolfram_script(process_dir, "calcloop_amplitude_squared.wl", code)
    wu.run_wolfram_script_simple(process_dir + "/calcloop_amplitude_squared.wl")
    return os.getcwd() + "/" + process_dir + "/ampSq/AmplitudeSquared"

def calcloop_family_decomposition(ampSq_file: str, process_dir: str = "cache"):
    code = f"""
If[$FrontEnd === Null, $InputFileName, NotebookFileName[]] // DirectoryName // SetDirectory;
Get["/home/huang/Downloads/MCPtest-main/calcloop-main/CalcLoop.wl"];
FamilyDecomposition["family", "{ampSq_file}"];
Quit[];
"""
    wu.create_wolfram_script(process_dir, "calcloop_family_decomposition.wl", code)
    wu.run_wolfram_script_simple(process_dir + "/calcloop_family_decomposition.wl")
    return os.getcwd() + "/" + process_dir + "/family/Families"

def calcloop_amflow_calculate_FI(family_file: str, numeric: str = "{}", process_dir: str = "cache"):
    code = f"""
If[$FrontEnd === Null, $InputFileName, NotebookFileName[]] // DirectoryName // SetDirectory;
Get["/home/huang/Downloads/MCPtest-main/calcloop-main/CalcLoop.wl"];
SetOptions[AMFlowCalculateFI, "Numeric"->{numeric}];
res = AMFlowCalculateFI["CalcFI", "{family_file}"]/.x_String :> ToExpression[x]/. CalcLoopSymbol[x__] :> x;
Put[res, "res"];
Quit[];
"""
    wu.create_wolfram_script(process_dir, "calcloop_amflow_calculate_FI.wl", code)
    wu.run_wolfram_script_simple(process_dir + "/calcloop_amflow_calculate_FI.wl")
    return os.getcwd() + "/" + process_dir + "/res"

if __name__ == "__main__":
    file = feynarts_create_amp("{F[1,1]} -> {F[1,1]}", 1)
    file = calcloop_amplitude_squared(file)
    file = calcloop_family_decomposition(file)
    file = calcloop_amflow_calculate_FI(file,"{ME->1,MM->1,ML->1}")
    print(file)
    
