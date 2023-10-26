import os
import sys
import shutil
from zipfile import ZipFile
from panoptic_segmentation.exception import AppException
from panoptic_segmentation.logger import logging
from panoptic_segmentation.entity.artifacts_entity import DataIngesionArtifacts
from panoptic_segmentation.entity.config_entity import DataIngestionConfig
import urllib
from tqdm import tqdm

class DataIngestion():
    def __init__(self, data_ingestion_config:DataIngestionConfig= DataIngestionConfig()):
        try:
            self.data_ingestion_config = DataIngestionConfig
        except Exception as e:
            logging.info(f"{AppException(e, sys)}")
            raise AppException(e, sys)
        
    def download_data(self):
        '''
        Download the dataset from the url
        '''
        try:
            logging.info(f"Downloading file from {self.data_ingestion_config.data_download_url}.\
                          This may take some time...")
            temp_path, _ = urllib.request.urlretrieve(self.data_ingestion_config.data_download_url)
            logging.info(f"Download successful!")
            return temp_path
        
        except Exception as e:
            logging.info(f"{AppException(e, sys)}")
            raise AppException(e, sys)
        
    def extract_files(self, temp_path):
        '''
        Unzip files from temporary location
        
        ARGS:
            temp_path: "str"
                Temporary path of the file downloaded
        '''
        try:
            logging.info(f"Creaing directory {self.data_ingestion_config.data_ingestion_dir}")
            os.makedirs(self.data_ingestion_config.data_ingestion_dir, exist_ok=True)

            logging.info(f"Directory created! unzipping files")
            with ZipFile(temp_path, "r") as f:
                f.extractall(self.data_ingestion_config.data_ingestion_dir)
            logging.info(f"Unzip Successful!")
            return self.data_ingestion_config.data_ingestion_dir
            
        except Exception as e:
            logging.info(f"{AppException(e, sys)}")
            raise AppException(e, sys)
        
    def initiate_data_ingestion(self)->DataIngesionArtifacts:
        '''
        Performs download as well asextraction of files
        '''
        try:
            zipfile_loc = self.download_data()
            data_loc = self.extract_files(zipfile_loc)

            data_ingestion_artifacts = DataIngesionArtifacts(
                data_zip_file_path= zipfile_loc,
                data_path= data_loc,
            )

        except Exception as e:
            raise AppException(e, sys)
