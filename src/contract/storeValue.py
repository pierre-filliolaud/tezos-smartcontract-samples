import smartpy as sp

class StoreValue(sp.Contract):
    def __init__(self, value):
        self.init(storedValue = value)
    @sp.entry_point
    def replace(self, params):
        self.data.storedValue = params
    @sp.entry_point
    def double(self):
        self.data.storedValue = self.data.storedValue * 2
    @sp.entry_point
    def divide(self, params):
        sp.verify(params != 0)
        self.data.storedValue = self.data.storedValue / params

# Tests   
@sp.add_test(name = "Test Store Value")
def test():
    scenario = sp.test_scenario()
    scenario.h1("Test Store Value")
    
    # We first define a contract and add it to the scenario
    c1 = StoreValue(12)
    scenario += c1 
    scenario += c1.double()
    scenario += c1.replace(4)
    scenario += c1.divide(3)
    
    # Finally, we check its final storage
    scenario.verify(c1.data.storedValue == 1)