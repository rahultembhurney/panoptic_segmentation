import sys, os
from panoptic_segmentation.exception import AppException
from panoptic_segmentation.logger import logging
from panoptic_segmentation.entity.config_entity import DatasetPreparationConfig
from panoptic_segmentation.entity.artifacts_entity import DataPreparationArtifacts
from panoptic_segmentation.components.dataset_preparation import DatasetPrepare
from panoptic_segmentation.constants.pipeline_constants import *


class PrepareData():
    def __init__(self):
        self.data_preparaion_config = DatasetPreparationConfig()

    def prepare_data(self)-> DataPreparationArtifacts:
        try:
            logging.info(f"Initiating data preparation pipeline")    
            data_preparation = DatasetPrepare()
            data_preparation_artifacts = data_preparation.create_dataloader(self.data_preparaion_config.data_dir+"/PASTIS")
            logging.info(f"Dataset preparation successful")
            return data_preparation_artifacts
        
        except Exception as e:
            logging.info(f"{AppException(e, sys)}")
            raise AppException(e, sys)
