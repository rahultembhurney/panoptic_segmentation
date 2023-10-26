import sys, os
from panoptic_segmentation.exception import AppException
from panoptic_segmentation.logger import logging
from panoptic_segmentation.entity.config_entity import DataIngestionConfig
from panoptic_segmentation.entity.artifacts_entity import DataIngesionArtifacts
from panoptic_segmentation.components.data_ingestion import DataIngestion


class IngestionPipeline():
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def ingest_data(self)->DataIngesionArtifacts:
        try:
            data_ingestion = DataIngestion()
            data_ingestion_arifacts = data_ingestion.initiate_data_ingestion()
            return data_ingestion_arifacts
        
        except Exception as e:
            logging.info(f"{AppException(e,sys)}")
            raise AppException(e, sys)
