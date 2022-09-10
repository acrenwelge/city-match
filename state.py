class State:

    def __init__(self,name,abbr,pop,tax_burden,econ_freedom,social_freedom):
        self.name = name
        self.abbr = abbr
        self.pop = pop
        self.tax_burden = tax_burden
        self.econ_freedom = econ_freedom
        self.social_freedom = social_freedom
    
    def __str__(self) -> str:
        return ",".join([self.name,"Pop:"+str(self.pop),"Tax Burden:"+str(self.tax_burden),
        "Economic Freedom:" + str(self.econ_freedom),"Social Freedom:" + str(self.social_freedom)])