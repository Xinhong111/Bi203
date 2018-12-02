data {
  // Number of data points for each experiment
  int N;
  // Number of entries in each level of the hierarchy
  int J_1;
  // Input of parameters of the priors
  real hyper_theta_mu;
  real hyper_theta_sigma;
  real hyper_sigma;
  real hyper_tau;
}


generated quantities {
  // Total number of data points 
  real n[N * J_1];
  // Priors
  real theta = normal_rng(hyper_theta_mu, hyper_theta_sigma);
  real sigma = fabs(normal_rng(0, hyper_sigma));
  real tau = fabs(normal_rng(0, hyper_tau));
  // Second layer
  real theta_1[J_1];  
  
  for (i in 1:J_1) {
    theta_1[i] = normal_rng(theta, sigma);
    for (j in 1:N) {
      n[(i - 1) * N + j] = normal_rng(theta_1[i], tau);
    }
  }
    
  }