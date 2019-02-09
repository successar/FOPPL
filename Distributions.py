from scipy.stats import norm, bernoulli

class Distribution() :
    def __init__(self) :
        self.distribution = True

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

distribution_constants = {
    'norm' : Normal,
    'bern' : Bernoulli
}
