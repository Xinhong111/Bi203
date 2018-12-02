data {
  int N;
  real n[N];
}


parameters {
  real<lower=0> a;
  real<lower=0> beta;
}


model {
  // Priors
  a ~ normal(0, 2);
  beta ~ normal(250, 80);

  // Likelihood
  n ~ weibull(a+1, beta);
}

generated quantities {
  real n_ppc[N];
  real log_lik[N];

  // Draw posterior predictive data set
  for (i in 1:N) {
    n_ppc[i] = weibull_rng(a+1 , beta);
  }
  
  // Compute pointwise log likelihood
  for (i in 1:N) {
    log_lik[i] = weibull_lpdf(n[i] | a+1 , beta);
  }
}