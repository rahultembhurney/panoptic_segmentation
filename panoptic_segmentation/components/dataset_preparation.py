import os, sys, shutil
from panoptic_segmentation.exception import AppException
from panoptic_segmentation.logger import logging
from panoptic_segmentation.constants.pipeline_constants import *
from panoptic_segmentation.entity.config_entity import DatasetPreparationConfig
from panoptic_segmentation.entity.artifacts_entity import DataPreparationArtifacts
import git


class DatasetPrepare():
    def __init__(self, data_preparation_config:DatasetPreparationConfig):
        self.data_preparation_config = data_preparation_config

    def clone_repo(self):
        '''
        Clones the pastis benchmark repor containing dataloaders
        '''
        try:
            logging.info(f"Cloning rep from {self.data_preparation_config.dataloader_download_url}")
            repo_url = self.data_preparation_config.dataloader_download_url
            os.makedirs(self.data_preparation_config.dataloader_dir, exist_ok=True)
            local_path = self.data_preparation_config.dataloader_dir
            repo = git.repo.clone_from(repo_url, local_path)
            logging.info(f"Cloning Successful")
            return local_path
        
        except Exception as e:
            logging.info(f"{AppException(e, sys)}")
            raise AppException(e, sys)
 
    def convert_repo_to_module(self):
        repo_path = self.clone_repo()
        with open(f"{repo_path}/__init__.py", "r") as f:
            pass
        with open(f"{repo_path}/code/__init__.py", "r") as f:
            pass


    

        
        
        
