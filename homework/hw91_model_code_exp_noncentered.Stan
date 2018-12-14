data {
  // Total number of data points
  int N;
  
  // Number of entries in each level of the hierarchy
  int J_1;

  //Index arrays to keep track of hierarchical structure
  int index_1[N];
  
  // The measurements
  real area[N];
  
  // Time
  vector[N] t;
}

parameters {
  // Hyperparameters level 0
  real a;
  real k;
  real<lower=0> sigma;

  // How hyperparameters vary
  real<lower=0> tau_a;
  real<lower=0> tau_k;

  // Hyperparameters level 1
  vector[J_1] a_1_tilde;
  vector[J_1] k_1_tilde;
}

transformed parameters {
  // Transformations for noncentered
  vector[J_1] a_1 = a + tau_a * a_1_tilde;
  vector[J_1] k_1 = k + tau_k * k_1_tilde;
  vector[N] area_temp;
  
  // Divide k by 100 when computing posterior
  for (i in 1:N) {
    area_temp[i] = a_1[index_1[i]] * exp(k_1[index_1[i]] * t[i] / 100);
  }
}

model {
  a ~ normal(1.4, 0.3);
  // 100 times larger prior for k and tau_k
  k ~ normal(1, 0.2);
  sigma ~ normal(0, 0.1);
  tau_a ~ normal(0, 0.1);
  tau_k ~ normal(0, 0.1);

  a_1_tilde ~ normal(0, 1);
  k_1_tilde ~ normal(0, 1);

  area ~ normal(area_temp, sigma);
}

generated quantities {
  vector[N] area_ppc;
  real log_lik[N];
  
  // Posterior predictive check
  for (i in 1:N) {
    area_ppc[i] = normal_rng(area_temp[i], sigma);
  }
  
  // Compute pointwise log likelihood
  for (i in 1:N) {
    log_lik[i] = normal_lpdf(area[i] | area_temp[i], sigma);
  }
}