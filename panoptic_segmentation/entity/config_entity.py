import os
from dataclasses import dataclass
from datetime import datetime
from panoptic_segmentation.constants.pipeline_constants import *

@dataclass
class DataIngestionConfig():
    data_ingestion_dir: str = os.path.join(
        ARTIFACTS_DIR, DATA_INGESTION_DIR_NAME

    )
    data_download_url:str = DATA_DOWNLOAD_URL

@dataclass
class DatasetPreparationConfig():
    data_dir: str = os.path.join(ARTIFACTS_DIR, DATA_INGESTION_DIR_NAME)
    # dataloader_download_url: str = PASTIS_BENCHMARK_URL
    # unet_paps_benchmark_dir: str = os.path.join(
    #     ARTIFACTS_DIR, UNET_PAPS_BENCHMARK_DIR
    # )