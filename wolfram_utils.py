import subprocess
import os
from typing import Tuple, Optional

def create_wolfram_script(directory: str, filename: str, content: str, encoding: str = 'utf-8') -> str:
    """
    Create a file with specified content in the given directory
    
    Args:
        directory (str): Target directory path
        filename (str): File name (*.wl)
        content (str): MMA code
        encoding (str): File encoding, default is utf-8
    
    Returns:
        str: Full path of the created file
    
    Raises:
        OSError: When directory creation or file writing fails
    """
    try:
        
        if not directory:
            directory = "."
        
        # Ensure the directory exists, create if it doesn't
        os.makedirs(directory, exist_ok=True)
        
        # Build the complete file path
        file_path = os.path.join(directory, filename)
        
        # Create file and write content
        with open(file_path, 'w', encoding=encoding) as file:
            file.write("(* ::Package:: *)\n\n" + content)
        
        print(f"File created successfully: {file_path}")
        return file_path
        
    except OSError as e:
        print(f"File creation failed: {e}")
        raise

def run_wolfram_script(script_path: str, timeout: Optional[int] = None) -> Tuple[int, str, str]:
    """
    Execute a Wolfram script using the 'wolfram -script' command
    
    Args:
        script_path (str): Path to the Wolfram script file (.wl or .m)
        timeout (Optional[int]): Timeout in seconds, None for no timeout
    
    Returns:
        Tuple[int, str, str]: (return_code, stdout, stderr)
            - return_code: Command exit code (0 for success)
            - stdout: Standard output from the script
            - stderr: Standard error output
    
    Raises:
        FileNotFoundError: When the script file doesn't exist
        subprocess.TimeoutExpired: When the command times out
        subprocess.SubprocessError: For other subprocess-related errors
    """
    try:
        # Check if script file exists
        if not os.path.isfile(script_path):
            raise FileNotFoundError(f"Script file not found: {script_path}")
        
        # Build the command
        command = ["wolfram", "-script", script_path]
        
        print(f"Executing: {' '.join(command)}")
        
        # Run the command
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return_code = result.returncode
        stdout = result.stdout
        stderr = result.stderr
        
        # Print execution result
        if return_code == 0:
            print("Script executed successfully")
        else:
            print(f"Script execution failed with return code: {return_code}")
        
        return return_code, stdout, stderr
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except subprocess.TimeoutExpired as e:
        print(f"Script execution timed out after {timeout} seconds")
        raise
    except subprocess.SubprocessError as e:
        print(f"Subprocess error: {e}")
        raise


def run_wolfram_script_simple(script_path: str) -> bool:
    """
    Simple version that only returns success/failure status
    
    Args:
        script_path (str): Path to the Wolfram script file
    
    Returns:
        bool: True if script executed successfully, False otherwise
    """
    try:
        return_code, _, _ = run_wolfram_script(script_path)
        return return_code == 0
    except Exception:
        return False

# Usage example
if __name__ == "__main__":
    # Example 1: Create a simple text file
    create_wolfram_script(
        directory="./test_dir",
        filename="test.wl",
        content="Put[\"Hello, World!\", \"hello.txt\"]\nQuit[]\n"
    )

    run_wolfram_script_simple("./test_dir/test.wl")