from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent, ImageContent, BlobResourceContents
import logging
import qft_functions as qft

# Set up logging (this just prints messages to your terminal for debugging)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create the MCP server object
mcp = FastMCP(host='localhost', port='3001', log_level='DEBUG')

# Here’s where you define your tools (functions the AI can use)
@mcp.tool()
def add(a: int, b: int) -> TextContent:
    """Add two numbers.

    Args:
        a: the first integer to be added
        b: the second integer to be added
    
    Return:
        The sum of the two integers, as a string."""
    return TextContent(type="text", text=str(a + b))

# The return format should be one of the types defined in mcp.types. The commonly used ones include TextContent, ImageContent, BlobResourceContents.
# In the case of a string, you can also directly use `return str(a + b)` which is equivalent to `return TextContent(type="text", text=str(a + b))`

@mcp.tool()
def get_image_of_flower():
    """Get an image of flower

    Return:
        Image of flower in png."""
    image_base64 = "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"
    # if you're not familiar with base64, you can see https://en.wikipedia.org/wiki/Base64

    return ImageContent(data=image_base64, mimeType="image/png", type="image")

@mcp.tool()
def create_feynman_amplitude(process: str, order: int) -> TextContent:
    """Create Feynman amplitude for a given process and order.
    Here is the symbol for the particles:
    F[1,{1}]: electron
    F[1,{2}]: muon
    F[1,{3}]: tau
    V[1]    : photon
    For anti-fermion, just add a minus sign before it, e.g. -F[1,{1}] is positron.

    Args:
        process: The particle process in the format "{A} -> {B}", e.g. "{F[1, {1}], -F[1, {1}]} -> {F[1, {2}], -F[1, {2}]}"
        order: The perturbative order, e.g. 0 for tree level, 1 for one-loop

    Returns:
        The path to the generated amplitude file on the server.
    """

    amp_path = qft.feynarts_create_amp(process, order)

    return TextContent(
        type="text",
        text=f"Amplitude file on the server created at: {amp_path}"
    )

@mcp.tool()
def amplitude_squared(amp_file1: str, amp_file2 = 1) -> TextContent:
    """Simplify the product of the first amplitude and the conjugate of the second amplitude.
    If the second amplitude is 1, it will just simplify the first amplitude.
    The file path is given by the function `feynarts_create_amp`.

    Args:
        amp_file1: The path to the first amplitude file on the server.
        amp_file2: The path to the second amplitude file on the server (1 by default).

    Returns:
        The path to the generated squared amplitude file on the server.
    """

    ampSq_path = qft.calcloop_amplitude_squared(amp_file1, amp_file2)

    return TextContent(
        type="text",
        text=f"Amplitude squared file on the server created at: {ampSq_path}"
    )

@mcp.tool()
def family_decomposition(ampSq_file: str) -> TextContent:
    """Perform family decomposition on the given amplitude squared file.
    The file path is given by the function `amplitude_squared`.

    Args:
        ampSq_file: The path to the amplitude squared file on the server.

    Returns:
        The path to the generated family decomposition file on the server.
    """

    family_path = qft.calcloop_family_decomposition(ampSq_file)

    return TextContent(
        type="text",
        text=f"Family decomposition file on the server created at: {family_path}"
    )

@mcp.tool()
def calculate_FI(family_file: str, numeric: str):
    """Calculate the FI for the given family decomposition file.
    The file path is given by the function `family_decomposition`.

    Args:
        family_file: The path to the family decomposition file on the server.
        numeric: The numeric value to use for the calculation, e.g. "{ME->1, MM->1, ML->1, s->100, t->-1}".
                 ME, MM, ML are the masses of electron, muon and tau respectively. s and t are the Mandelstam variables.

    Returns:
        The numerical result.
    """

    res_path = qft.calcloop_amflow_calculate_FI(family_file, numeric)
    with open(res_path, 'r') as f:
        res = f.read()

    return TextContent(
        type="text",
        text=f"The numerical result is: {res}"
    )

# This is the main entry point for your server
def main():
    logger.info('Starting your-new-server')
    mcp.run(transport='streamable-http')

if __name__ == "__main__":
    main()