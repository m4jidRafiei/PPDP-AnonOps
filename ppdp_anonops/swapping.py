from anonymizationOperations import anonymizationOperationInterface

class Swapping_AO(anonymizationOperationInterface):
    def __init__(self):
        #self.name = name
        pass

    def Process(self, xes_path: str, parameter) -> str:
        result = None
        return {'Operation': 'Swapping', 'Result': result}
        pass