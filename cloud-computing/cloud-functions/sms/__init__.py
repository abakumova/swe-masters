import logging
import json

import azure.functions as func


def main(documents: func.DocumentList, message: func.Out[str]) -> str:
    logging.info("Function")
    value = {
      "body": "Message!",
      "To": "+372"
    }

    message.set(json.dumps(value))