data { 
  real a;
  real b;
  int Nt;
  int n;
}


parameters {
  real<lower=0, upper=1> theta;
}


model {
  // Priors
  theta ~ beta(a, b);

  // Likelihood
  n ~ binomial(Nt, theta);
}