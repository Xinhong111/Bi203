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
  real theta;
  real<lower=0> sigma;

  // How hyperparameters vary
  real<lower=0> tau;

  // Hyperparameters level 1
  vector[J_1] theta_1;
}


model {
  theta ~ normal(1, 0.3);
  sigma ~ normal(0, 0.1);
  tau ~ normal(0, 0.1);

  theta_1 ~ normal(theta, tau);

  assay_result ~ normal(theta_1[index_1], sigma);
}