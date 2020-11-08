import smartpy as sp

class BasicCrowdfunding(sp.Contract):
    def __init__(self, owner):
        self.init(
            admin = owner,
            contributedAmount = sp.tez(0)
            )
        
    @sp.entry_point
    def addFunds(self):
        self.data.contributedAmount += sp.amount
    
    @sp.entry_point
    def cashoutFunds(self):
        sp.verify(sp.sender == self.data.admin)
        sp.send(sp.sender, self.data.contributedAmount)

@sp.add_test(name = "BasicCrowdfundingTest")
def test():
    scenario = sp.test_scenario()
    scenario.h1("Basic Crowfunding Testing")
    
    scenario.h2("[TEST] Initiating the contract")
    
    owner = sp.address("tz1-owner-address")
    someoneElse = sp.address("tz1-someoneElseAddress")
    
    c1 = BasicCrowdfunding(owner)
    scenario += c1
    
    scenario.h2("[TEST] Sending funds")
    
    Alice = sp.test_account("Alice")
    Bob = sp.test_account("Bob")
    Elie = sp.test_account("Elie")
    
    scenario.h3("Alice participates in the crowdfunding")
    scenario += c1.addFunds().run(sender = Alice, amount = sp.tez(100))
    
    scenario.h3("Bob participates in the crowdfunding")
    scenario += c1.addFunds().run(sender = Bob, amount = sp.tez(35))
    
    scenario.h3("Elie participates in the crowdfunding")
    scenario += c1.addFunds().run(sender = Elie, amount = sp.tez(250))
    
    scenario.h2("[TEST] Owner cashing out funds - should work")
    scenario += c1.cashoutFunds().run(sender = owner)
    
    scenario.h2("[TEST] Someone else cashing out funds - should not work")
    scenario += c1.cashoutFunds().run(sender = someoneElse, valid = False)