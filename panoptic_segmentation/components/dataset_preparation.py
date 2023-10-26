import os, sys, shutil
from panoptic_segmentation.exception import AppException
from panoptic_segmentation.logger import logging
from panoptic_segmentation.constants.pipeline_constants import *
from panoptic_segmentation.entity.config_entity import DatasetPreparationConfig
from panoptic_segmentation.entity.artifacts_entity import DataPreparationArtifacts
from panoptic_segmentation.utils.main_utils import clone_repo
import torch
try:
    from artifacts.pastis_benchmark.code import dataloader
    from artifacts.pastis_benchmark.code.collate import pad_collate
except Exception as e:
    clone_repo(repo_path=PASTIS_BENCHMARK_URL, local_path=UNET_PAPS_BENCHMARK_DIR)
    from artifacts.pastis_benchmark.code import dataloader
    from artifacts.pastis_benchmark.code.collate import pad_collate




class DatasetPrepare():
    def __init__(self, data_preparation_config:DatasetPreparationConfig = DatasetPreparationConfig()):
        self.data_preparation_config = data_preparation_config

    def create_dataset(self,
                       folder,
                       norm=True, target="semantic",
                       cache=False, mem16=False,
                       folds=None,
                       reference_date="2018-09-01",
                       class_mapping=None,
                       mono_date=None,
                       sats=["S2"],
                       ):
        """
        Pytorch Dataset class to load samples from the PASTIS dataset, for semantic and
        panoptic segmentation.

        The Dataset yields ((data, dates), target) tuples, where:
            - data contains the image time series
            - dates contains the date sequence of the observations expressed in number
              of days since a reference date
            - target is the semantic or instance target

        Args:
            folder (str): Path to the dataset
            norm (bool): If true, images are standardised using pre-computed
                channel-wise means and standard deviations.
            reference_date (str, Format : 'YYYY-MM-DD'): Defines the reference date
                based on which all observation dates are expressed. Along with the image
                time series and the target tensor, this dataloader yields the sequence
                of observation dates (in terms of number of days since the reference
                date). This sequence of dates is used for instance for the positional
                encoding in attention based approaches.
            target (str): 'semantic' or 'instance'. Defines which type of target is
                returned by the dataloader.
                * If 'semantic' the target tensor is a tensor containing the class of
                  each pixel.
                * If 'instance' the target tensor is the concatenation of several
                  signals, necessary to train the Parcel-as-Points module:
                    - the centerness heatmap,
                    - the instance ids,
                    - the voronoi partitioning of the patch with regards to the parcels'
                      centers,
                    - the (height, width) size of each parcel
                    - the semantic label of each parcel
                    - the semantic label of each pixel
            cache (bool): If True, the loaded samples stay in RAM, default False.
            mem16 (bool): Additional argument for cache. If True, the image time
                series tensors are stored in half precision in RAM for efficiency.
                They are cast back to float32 when returned by __getitem__.
            folds (list, optional): List of ints specifying which of the 5 official
                folds to load. By default (when None is specified) all folds are loaded.
            class_mapping (dict, optional): Dictionary to define a mapping between the
                default 18 class nomenclature and another class grouping, optional.
            mono_date (int or str, optional): If provided only one date of the
                available time series is loaded. If argument is an int it defines the
                position of the date that is loaded. If it is a string, it should be
                in format 'YYYY-MM-DD' and the closest available date will be selected.
            sats (list): defines the satellites to use. If you are using PASTIS-R, you have access to
                Sentinel-2 imagery and Sentinel-1 observations in Ascending and Descending orbits,
                respectively S2, S1A, and S1D.
                For example use sats=['S2', 'S1A'] for Sentinel-2 + Sentinel-1 ascending time series,
                or sats=['S2', 'S1A','S1D'] to retrieve all time series.
                If you are using PASTIS, only  S2 observations are available.
        """
        try:
            logging.info(f"Creating Pastis dataset")
            data = dataloader.PASTIS_Dataset(
            folder=folder,
            norm=norm,
            target=target,
            cache=cache,
            folds=folds,
            reference_date = reference_date,
            class_mapping=class_mapping,
            mono_date=mono_date,
            sats=sats,
        )
            logging.info(f"Pastis dataset successfully created")
            return data
        
        except Exception as e:
            logging.info(f"{AppException(e, sys)}")
            raise AppException(e, sys)
        
        
    
    def create_dataloader(self,
                          folder,
                          batch_size=2,
                          collate_fn=pad_collate,
                          shuffle=True,
                          norm=True, target="semantic",
                          cache=False, mem16=False,
                          folds=None,
                          reference_date="2018-09-01",
                          class_mapping=None,
                          mono_date=None,
                          sats=["S2"],):
        try:
            logging.info(f"creating Pastis dataloader")
            data = self.create_dataset(folder=self.data_preparation_config.data_dir + "/PASTIS",
                                       norm=norm,
                                       cache=cache, mem16=mem16,
                                       folds=folds,
                                       reference_date=reference_date,
                                       class_mapping=class_mapping,
                                       mono_date=mono_date,
                                       sats=sats)
            dataset = torch.utils.data.DataLoader(data, batch_size=batch_size,
                                              collate_fn=collate_fn,
                                              shuffle=shuffle)
        
            return dataset
        except Exception as e:
            logging.info(f"{AppException(e, sys)}")
            raise AppException(e, sys)

        

    


    


    

        
        
        
