from dataclasses import dataclass

@dataclass
class DataIngesionArtifacts():
    data_zip_file_path: str
    data_path: str


@dataclass
class DataPreparationArtifacts():
    dataset_dir: str
