from panoptic_segmentation.logger import logging
from panoptic_segmentation.exception import AppException
import sys
from panoptic_segmentation.pipeline.ingestion_pipeline \
                                            import IngestionPipeline

logging.info(f"Custom logger working successfully")

# try:
#     a = 4/str(6)
# except Exception as e:
#     logging.info(f"{AppException(e, sys)}")
#     raise AppException(e, sys)

ingestion_obj = IngestionPipeline()
ingestion_obj.ingest_data()
logging.info(f"Done Ingesting")
print(f"Done Ingesting")



