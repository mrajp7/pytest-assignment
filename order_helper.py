import json

class Orders:
    """
    This class is a wrapper to store and read the orders
    """
    _instance = None
    

    def __init__(self, order_file_path: str = "elastic_data.json"):
        if order_file_path:
            with open(order_file_path) as order_file:
                self.data = json.load(order_file)
        else:
            self.data = "" # could be from API or other sources if not from elastic file
        self.list = self.data['hits']['hits']
        self.__class__._instance = self

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance