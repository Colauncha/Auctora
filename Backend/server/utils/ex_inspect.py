import inspect

class ExtInspect(inspect.Signature):
    def __init__(self, class_name: str = None):
        self.class_name = class_name

    def info(self):
        module_name = inspect.stack()[1].frame.f_globals["__name__"]
        method_name = inspect.stack()[1].function
        caller_name = inspect.stack()[2].function
        line = inspect.currentframe().f_back.f_lineno
        trace_info = self.trace(skip=2)
        info = {
            'class_name': self.class_name,
            'module_name': module_name,
            'method_name': method_name,
            'caller_name': caller_name,
            'line': line,
            'trace_info': trace_info
        }
        print(info, end="\n\n")
        return info
    
    def trace(self, skip=0):
        stack = inspect.stack()
        len_stack = len(stack)
        trace_info = []
        for i in range(skip, len_stack):
            frame_info = stack[i]
            method_name = frame_info.function
            line_no = frame_info.lineno
            method_name = f"{method_name}({line_no})"
            trace_info.append(method_name)
        return trace_info

    def line_no(self):
        return inspect.currentframe().f_back.f_lineno
