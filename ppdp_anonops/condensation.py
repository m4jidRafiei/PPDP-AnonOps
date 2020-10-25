from anonymizationOperations import anonymizationOperationInterface


class Condensation_AO(anonymizationOperationInterface):
    def __init__(self):
        #self.name = name
        pass

    def Process(self, xes_path: str, parameter) -> str:
        result = None
        return {'Operation': 'Condensation', 'Result': result}
        pass
