data {
  int N;
  real n[N];
}


parameters {
  real<lower=0> a;
  real<lower=0> b;
}


transformed parameters {
  real beta_ = 1.0 / b;
}


model {
  // Priors
  a ~ normal(1, 0.5);
  b ~ normal(250.0, 80.0);;

  // Likelihood
  n ~ gamma(a, beta_);
}


generated quantities {
  real n_ppc[N];
  real log_lik[N];

  // Draw posterior predictive data set
  for (i in 1:N) {
    n_ppc[i] = gamma_rng(a, beta_);
  }
  
  // Compute pointwise log likelihood
  for (i in 1:N) {
    log_lik[i] = gamma_lpdf(n[i] | a, beta_);
  }
}