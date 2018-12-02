data {
  int N;
  real a_0_phi;
  real a_0_sigma;
  real beta_0_phi;
  real beta_0_sigma;
}


generated quantities {
  // Parameters
  real<lower=0> a;
  real<lower=0> beta;

  // Data
  real ell[N];

  a = normal_rng(a_0_phi, a_0_sigma);
  beta = normal_rng(beta_0_phi, beta_0_sigma);

  for (i in 1:N) {
    ell[i] = gamma_rng(a, 1/beta);
  }
}