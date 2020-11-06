# Place this file in ~/.ipython/profile_default/startup/ directory
# to add support for PowerShell commands in IPython
#
# Original code taken from:
# http://stackoverflow.com/questions/19644926/configure-ipython-to-use-powershell-instead-of-cmd
#

from IPython.core.magic import register_line_cell_magic
from IPython import get_ipython

ipython = get_ipython()

@register_line_cell_magic
def ps(line, cell=None):
    "Magic that works both as %ps and as %%ps" 
    if cell is None:
        ipython.run_cell_magic('powershell', '--out posh_output', line)
        return posh_output.splitlines()
    else:
        return ipython.run_cell_magic('powershell', line, cell)
