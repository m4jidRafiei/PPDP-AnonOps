from anonymizationOperations import anonymizationOperationInterface

class Generalization_AO(anonymizationOperationInterface):
    def __init__(self):
        #self.name = name
        pass

    def Process(self, xes_path: str, parameter) -> str:
        result = None
        return {'Operation': 'Generalization', 'Result': result}
        pass