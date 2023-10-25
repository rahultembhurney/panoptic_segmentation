from panoptic_segmentation.logger import logging
from panoptic_segmentation.exception import AppException
import sys

logging.info(f"Custom logger working successfully")

try:
    a = 4/str(6)
except Exception as e:
    logging.info(AppException(e, sys))
    raise AppException(e, sys)