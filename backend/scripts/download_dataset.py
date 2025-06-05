import kagglehub
import shutil
from pathlib import Path

print("Realizando download dataset TMDB")

path = kagglehub.dataset_download("asaniczka/tmdb-movies-dataset-2023-930k-movies/versions/590")

csv_files = list(Path(path).glob("*.csv"))
if not csv_files:
    print("Nenhum arquivo CSV encontrado.")
    exit(1)

csv_arquivo = csv_files[0]

destino = Path("data/tmdb-movies.csv")
destino.parent.mkdir(parents=True, exist_ok=True)
shutil.copy(csv_arquivo, destino)

print(f"Dataset movido para: {destino.resolve()}")
