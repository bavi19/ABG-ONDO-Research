"""Execute using this Python interpreter; no global kernel registration required."""
import os
from pathlib import Path
import sys
import tempfile
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

ROOT = Path(__file__).resolve().parents[1]
runtime = ROOT / '.runtime'
runtime.mkdir(exist_ok=True)
for key in ('JUPYTER_RUNTIME_DIR', 'IPYTHONDIR', 'MPLCONFIGDIR', 'TEMP', 'TMP'):
    path = runtime / key.lower()
    path.mkdir(exist_ok=True)
    os.environ[key] = str(path)
tempfile.tempdir = str(runtime / 'temp')
Path(tempfile.tempdir).mkdir(exist_ok=True)
notebook = ROOT / 'notebooks/ONDO_Analysis.ipynb'
nb = nbformat.read(notebook, as_version=4)
km = KernelManager(connection_file=str(runtime / 'kernel.json'))
km.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
client = NotebookClient(nb, km=km, timeout=180, resources={'metadata': {'path': str(ROOT / 'notebooks')}})
try:
    with client.setup_kernel(cwd=str(ROOT / 'notebooks')):
        client.execute()
finally:
    if km.has_kernel:
        km.shutdown_kernel(now=True)
nbformat.write(nb, notebook)
print('Executed ONDO_Analysis.ipynb successfully; all cells completed.')
