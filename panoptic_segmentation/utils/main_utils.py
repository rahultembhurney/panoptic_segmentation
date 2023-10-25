import torch 
import os
import json
from argparse import Namespace

import matplotlib
import matplotlib.pyplot as plt 
from matplotlib.colors import ListedColormap

from matplotlib import patches
import numpy as np 
import sys
from panoptic_segmentation.logger import logging
from panoptic_segmentation.exception import AppException

cm = matplotlib.colormaps["tab20"]
def_colors = cm.colors
cus_colors = ["k"] + [def_colors[i] for i in range(1,20)] + ["w"]
cmap = ListedColormap(colors=cus_colors, N=21)

def get_rgb(x,batch_id=0, tshow=1):
    '''
    Utility function to display satellite images from sentinel 2 time series 
    
    ARGS:
        x: Train data

        batch_id: default=0 | type=int 
            Batch id  to generate image from.
        
        tshow: default=1 | type=int
            index of time-series to display from specified batch.
    '''
    try:
        im = x["S2"][batch_id, tshow,[2,1,0]].cpu().numpy()
        mx = im.max(axis=(1,2))
        mi = im.min(axis=(1,2))
        im = im-mi/mx-mi[:, None, None]
        im = im.swapaxes(0,2).swapaxes(0,1)
        im = np.clip(im, a_min=0, a_max=1)
        return im
    except Exception as e:
        logging.info(f"{AppException(e, sys)}")
        raise AppException(e, sys)

    

def get_radar(x, batch_id=0, tshow=1, orbit="D"):
    """
    Utility function to get a displayable image from a Sentinel-1 time series.
    
    ARGS:
        x: Train data

        batch_id: default=0 | type=int 
            Batch id  to generate image from.
        
        tshow: default=1 | type=int
            index of time-series to display from specified batch.

        orbit: default="D" | type = str
            type of orbit
    """
    try:
        im = x["S1{}".format(orbit)][batch_id, tshow].cpu().numpy()
        mx = im.max(axis=(1,2))
        mi = im.min(axis=(1,2))
        im = im-mi/mx-mi[:, None, None]
        im = im.swapaxes(0,2).swapaxes(0,1)
        im = np.clip(im, a_max=1, a_min=0)
        return im
    except Exception as e:
        logging.info(f"{AppException(e, sys)}")
        raise AppException(e, sys)

def plot_images(dataset, t_show, batch_index):
    '''
    Plots series of images for the specified batch

    ARGS:
        dataset: Dataset to generate images from.
            Note: Dataset processed only by "PASTIS_Dataset" dataloader should be passed as the parameter here.

        batch_id: default=0 | type=int 
            Batch id  to generate image from.
        
        t_show: default=1 | type=int
            Number of time-series images starting from "0"th index to display from specified batch.

    '''
    try:
        (x, dates), y = dataset.__iter__().__next__()
        (
            target_heatmap,
            instance_ids,
            pixel_to_instance_mapping,
            instance_bbox_size,
            object_semantic_annotation,
            pixel_semantic_annotation,
        ) = y.split((1,1,1,2,1,1), dim=-1)

        for t in range(t_show):
            bid = batch_index

            fig, axes = plt.subplots(1,4, figsize=(20,20))

            axes[0].imshow(get_rgb(x, batch_id=bid, t_show=t))
            axes[1].imshow(target_heatmap[bid].squeeze())
            axes[2].imshow(instance_ids[bid].squeeze(), cmap="prism", alpha=0.6)
            axes[3].imshow(pixel_semantic_annotation[bid].squeeze(), cmap=cmap, vmin=0,\
                        vmax=20)

            axes[0].set_title("One S2 Observation.")
            axes[1].set_title("Centerness Ground Truth.")
            axes[2].set_title("Instance masks.")
            axes[3].set_title("Semantic Labels")

    except Exception as e:
        logging.info(f"{AppException(e, sys)}")
        raise (AppException(e, sys))

