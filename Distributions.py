from scipy.stats import norm, bernoulli, rv_discrete

class Distribution() :
    distribution = True
    def __init__(self) :
        pass

class Normal(Distribution) :
    def __init__(self, loc, scale) :
        super(Normal, self).__init__()
        self.loc = loc
        self.scale = scale

    def sample(self) :
        return norm.rvs(self.loc, self.scale)

    def logpdf(self, x) :
        return norm.logpdf(x, self.loc, self.scale)

class Bernoulli(Distribution) :
    def __init__(self, p) :
        super(Bernoulli, self).__init__()
        self.p = p

    def sample(self) :
        return bernoulli.rvs(self.p)

    def logpdf(self, x) :
        return bernoulli.logpmf(x, self.p)
    
class Discrete(Distribution) :
    def __init__(self, vec) :
        super(Discrete, self).__init__()
        self.vec = vec
        
    def sample(self) :
        return rv_discrete(values=(range(len(self.vec)), self.vec)).rvs()
    
    def logpdf(self, x) :
        return rv_discrete(values=(range(len(self.vec)), self.vec)).logpmf(x)

distribution_constants = {
    'norm' : Normal,
    'bern' : Bernoulli,
    'discrete' : Discrete,
    'p_norm' : lambda v, l, s : Normal(l, s).logpdf(v),
    'p_bern' : lambda v, p : Bernoulli(p).logpdf(v),
    'p_discrete' : lambda v, vec : Discrete(vec).logpdf(v)
}
