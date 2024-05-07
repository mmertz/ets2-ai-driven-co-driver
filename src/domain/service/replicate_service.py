import logging
import os
from typing import Dict, Optional

import replicate

from src.config import REPLICATE_API_KEY

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_KEY


def make_replicate_prediction(
    model_version: str, input_data: Dict, is_stream: bool
) -> Optional[Dict]:
    try:
        output = replicate.run(model_version, input=input_data)

        if is_stream:
            combined_output = ""
            for event in output:
                combined_output += event

            return combined_output

        return output
    except Exception as e:
        logging.error(f"Failed to make prediction with Replicate: {str(e)}")
        return None
