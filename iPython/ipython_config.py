#
# ipython_config.py
#

c = get_config()

# setup powershell
c.ScriptMagics.script_magics = ['powershell']
c.ScriptMagics.script_paths = {
	'powershell': 'powershell.exe -noprofile -command -'}



