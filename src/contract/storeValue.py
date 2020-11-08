# importing the library SmartPy
import smartpy as sp

# class definition which inherits from sp.Contract
class StoreValue(sp.Contract):
    # __init__ constructor which will call self.init() in order to, 
    # as we can see from the name of the function, initialize all 
    # the fields we have in our contract’s storage.
    def __init__(self, value):
        self.init(
            # initializing field storedValue
            storedValue = value
            )

    # An entry point is a method of a contract class 
    # that can be called from the outside
    @sp.entry_point
    def replace(self, params):
        self.data.storedValue = params.value

    @sp.entry_point
    def double(self):
        self.data.storedValue = self.data.storedValue * 2

    @sp.entry_point
    def divide(self, params):
        sp.verify(params.value != 0)
        self.data.storedValue = self.data.storedValue / params.value

    @sp.entryPoint
    def computeSum(self, params):
        self.data.storedValue = params.augend + params.addend

# Tests   
@sp.add_test(name = "Test Store Value")
def test():
    scenario = sp.test_scenario()
    scenario.h1("Test Store Value")
    
    # We first define a contract and add it to the scenario
    contract = StoreValue(12)
    scenario += contract 
    scenario += contract.double()
    scenario += contract.replace(value=4)
    scenario += contract.divide(value=3).run(sender = sp.address("tz1234"))
    
    # Finally, we check its final storage
    scenario.verify(contract.data.storedValue == 1)

    scenario += contract.computeSum(augend = 1, addend = 2).run(sender = sp.address("tz1234"))