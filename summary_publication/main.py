from src.agents.summarizer import SummaryPublication

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

SummaryPublication(system_name="astrea", client_name="franco").generate()
