from abc import ABC, abstractmethod


class BillGenerator(ABC):
    @abstractmethod
    def generate_bill(self, data):
        pass

    @abstractmethod
    def download_bill(self, bill_id):
        pass
