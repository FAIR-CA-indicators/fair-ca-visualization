from pathlib import Path

__author__ = "Matthias König"
__version__ = "0.1.0"

BASE_PATH = Path(__file__).parent.parent.parent
DATA_PATH = BASE_PATH / "data"

TEMPLATE_PATH = DATA_PATH / "FAIR_assessment_template.xlsx"
