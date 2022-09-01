import concurrent.futures

class ReturnValue():
    def __init__(self, return_value_1, return_value_2):
        self.return_value_1 = return_value_1
        self.return_value_2 = return_value_2
        
    def show_value_1(self):
        return self.return_value_1
    
    def show_value_2(self):
        return self.return_value_2


class MultiThread():
    def __init__(self) -> None:
        pass

    @classmethod
    def multi_thread(cls, method_1, method_2, **kwargs):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            m1 = executor.submit(method_1, **kwargs)
            m2 = executor.submit(method_2, **kwargs)
            return_value = ReturnValue(m1.result(), m2.result())
        return return_value
    
# end of line break
