data {
  int N;
  real beta_0_phi;
  real beta_0_sigma;
}


generated quantities {
  // Parameters
  real<lower=0> beta;

  // Data
  real ell[N];

  beta = normal_rng(beta_0_phi, beta_0_sigma);

  for (i in 1:N) {
    ell[i] = exponential_rng(1/beta);
  }
}