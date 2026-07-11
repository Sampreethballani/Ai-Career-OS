from abc import ABC, abstractmethod
from src.utils.logger import setup_logger

class BaseAgent(ABC):
    def __init__(self, name):
        self.name = name
        self.logger = setup_logger(name, f'logs/{name}.log')

    @abstractmethod
    def fetch_opportunities(self):
        """
        Fetches opportunities from the source.
        Should return a list of dictionaries containing opportunity details.
        """
        pass

    def run(self):
        self.logger.info(f"Starting {self.name} fetch...")
        try:
            opportunities = self.fetch_opportunities()
            self.logger.info(f"Found {len(opportunities)} opportunities.")
            return opportunities
        except Exception as e:
            self.logger.error(f"Error in {self.name}: {e}")
            return []
