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
    

            
if __name__ == '__main__':
    import time
    
    class Container():
        def __init__(self, first_val, second_val):
            self.first_val = first_val
            self.second_val = second_val
            
    
    class F1():
        def __init__(self):
            pass
         
        def func_1(self, **kwargs):
            print('func_1 starts')
            a = kwargs['product_code']
            b = kwargs['target_timestamp']
            addition = a + b
            time.sleep(5)
            subduction = a - b
            result = Container(addition, subduction)
            print('func_1 ends')
            return result

    class F2():
        def __init__(self):
            pass
            
        def func_2(self, **kwargs):
            print('func_2 starts')
            c = kwargs['product_code']
            d = kwargs['target_timestamp']
            addition = c + d
            time.sleep(2)
            multiplication = c * d
            result = Container(addition, multiplication)
            print('func_2 ends')
            return result

    class F3():
        def func_3(self, **kwargs):
            print('func_3 starts')
            e = kwargs['product_code']
            print(f"e = {e}")
            time.sleep(1)
            print('func_3 ends')

    class F4():
        def func_4(self, **kwargs):
            print('func_4 starts')
            g = kwargs['product_code']
            h = kwargs['target_timestamp']
            result = g / h
            time.sleep(3)
            print('func_4 ends')
            return result
    
        
    obj_1 = F1()
    obj_2 = F2()
    mt = MultiThread()
    rval = mt.multi_thread(obj_1.func_1, obj_2.func_2, product_code = 2, target_timestamp = 5)
    print(rval.show_value_1().first_val)
    print(rval.show_value_1().second_val)
    print(rval.show_value_2().first_val)
    print(rval.show_value_2().second_val)
    
    obj_3 = F3()
    obj_4 = F4()
    mt_2 = MultiThread()
    rval_2 = mt_2.multi_thread(obj_3.func_3, obj_4.func_4, product_code = 2, target_timestamp = 5)
    print(rval_2.show_value_1())
    print(rval_2.show_value_2())
