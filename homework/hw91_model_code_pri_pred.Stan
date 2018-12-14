data {
  // Total Number of data points 
  int N;
  
  // Number of entries in each level of the hierarchy
  int J_1;
  int J_2;
  vector[N] t;
  
  
  // Input of parameters of the priors
  real hyper_a0_mu;
  real hyper_a0_sigma;
  
  real hyper_k0_mu;
  real hyper_k0_sigma;
  
  real hyper_a0_tau;
  real hyper_k0_tau;
  
  real hyper_sigma;
}


generated quantities {
  // Total number of data points 
  real area[N * J_1];
  
  // Priors
  real a0 = normal_rng(hyper_a0_mu, hyper_a0_sigma);
  real k0 = normal_rng(hyper_k0_mu, hyper_k0_sigma);
  
  real a0_tau = fabs(normal_rng(0, hyper_a0_tau));
  real k0_tau = fabs(normal_rng(0, hyper_k0_tau));
  
  real sigma = fabs(normal_rng(0, hyper_sigma));
  
  // Second layer
  real a_1[J_1]; 
  real k_1[J_1];
  
  for (i in 1:J_1) {
    a_1[i] = normal_rng(a0, a0_tau);
    k_1[i] = normal_rng(k0, k0_tau);
    for (j in 1:N) {
      area[(i - 1) * N + j] = normal_rng((a_1[i] + k_1[i] * t[j]), sigma);
  }
  }
  
  }