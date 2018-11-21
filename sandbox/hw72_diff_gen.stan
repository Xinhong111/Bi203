data { 
  real a1;
  real b1;
  real a2;
  real b2;
  int Nt1;
  int n1;
  int Nt2;
  int n2;
}


parameters {
  real<lower=0, upper=1> theta1;
  real<lower=0, upper=1> theta2;
}


model {
  // Priors
  theta1 ~ beta(a1, b1);
  theta2 ~ beta(a2, b2);

  // Likelihood
  n1 ~ binomial(Nt1, theta1);
  n2 ~ binomial(Nt2, theta2);
}

generated quantities {
  real dtheta = theta2 - theta1;
}