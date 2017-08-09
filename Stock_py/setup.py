from distutils.core import setup
import py2exe
import matplotlib

includes = ['os', 'sys', 'time']
packages = ['requests', 'bs4', 'Tkinter', 'tkMessageBox', 'webbrowser', 'functools', 'matplotlib', 'FileDialog']
# for matplotlib
excludes = ['libgdk_pixbuf-2.0-0.dll', 'libgobject-2.0-0.dll',  'libgdk-win32-2.0-0.dll']

datafiles = [r'C:\Python27\Lib\site-packages\requests\cacert.pem']
datafiles.extend(matplotlib.get_py2exe_datafiles())

setup(
	windows = ['stock_ui.py'],
	#console = ['tk_ui.py'],
	options = {'py2exe': {'packages':packages,
						  'includes':includes,
						  'dll_excludes':excludes}},
	data_files = datafiles
	)
