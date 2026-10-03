import sys
from pathlib import Path

src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from company_pre_crew.gradio_app import run_gui

run_gui()