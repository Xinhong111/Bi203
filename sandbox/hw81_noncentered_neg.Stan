data {
  // Total number of data points
  int N;
  
  // Number of entries in each level of the hierarchy
  int J_1;

  //Index arrays to keep track of hierarchical structure
  int index_1[N];
  
  // The measurements
  real assay_result[N];
}


parameters {
  // Hyperparameters level 0
  real<lower=0> theta;
  real<lower=0> sigma;

  // How hyperparameters vary
  real<lower=0> tau;

  // Hyperparameters level 1
  vector[J_1] theta_1_tilde;
}

transformed parameters {
  // Transformations for noncentered
  vector[J_1] theta_1 = theta + tau * theta_1_tilde;
}

model {
  theta ~ normal(0, 0.05);
  sigma ~ normal(0, 0.01);
  tau ~ normal(0, 0.01);

  theta_1_tilde ~ normal(0, 1);

  assay_result ~ normal(theta_1[index_1], sigma);
}