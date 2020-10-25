from anonymizationOperations import anonymizationOperationInterface

class Addition_AO(anonymizationOperationInterface):
    """Extract text from a PDF."""

    def __init__(self):
        #self.name = name
        pass

    def Process(self, xes_path: str, parameter) -> str:
        xes_log = xes_importer_factory.apply(xes_path)
        no_traces = len(xes_log)
        no_events = sum([len(trace) for trace in xes_log])

        result = self.get_attributes(xes_log)



#    log[0] refers to the first trace in the log
#        log[0][0] refers to the first event of the first trace in the log
#            log[0][1] refers to the second event of the first trace in the log
#    log[1] refers to the second trace in the log
#        log[1][0] refers to the first event of the second case in the log
#        log[1][1] refers to the second event of the second case in the log


        return {'Operation': 'Addition', 'Result': result}
        pass

    def get_attributes(self, xes_log):
        sensitives = []
        case_attribs = []
        for case_index, case in enumerate(xes_log):
            for key in case.attributes.keys():
                if key not in case_attribs:
                    case_attribs.append(key)

        event_attribs = []
        for case_index, case in enumerate(xes_log):
            for event_index, event in enumerate(case):
                for key in event.keys():
                    if key not in event_attribs:
                        event_attribs.append(key)

        sensitives = case_attribs + event_attribs
        sensitives.sort()
        # sensitives = case_attribs
        print("in function")
        print(sensitives)
        return sensitives
