from pathlib import Path

# Directories
BASE_DIR = Path(__file__).parent.parent.absolute()
CONFIG_DIR = Path(BASE_DIR, 'config')
DATA_DIR = Path(BASE_DIR, 'datasets')

# URls
DATA_URL = 'https://resultados.valenciaciudaddelrunning.com/en/maraton-clasificados.php?y=2022'

# Create directories
DATA_DIR.mkdir(parents=True, exist_ok=True)
