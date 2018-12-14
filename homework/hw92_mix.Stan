data {
  // Number of datapoints
  int N;
  // Conc of a
  int ca0;
  // Conc of b
  real cb0[N];
  // Measured fluorescence
  real F[N];
}


parameters {
  real<lower=0> Kd;
  real<lower=0> f0;
  real<lower=0> fq;
  positive_ordered[2] noise;
  real<lower=0, upper=1> w[N];
}

transformed parameters {
  real F_temp[N];
  for (i in 1:N) {
  // Generate calculated F for each point
    F_temp[i] = f0 * ca0 - (2 * (f0 - fq) * ca0 * cb0[i]) / (Kd + ca0 + cb0[i] + sqrt((Kd + ca0 + cb0[i])^2 - 4 * ca0 * cb0[i]));
  }
}


model {
  Kd ~ normal(0, 100);
  f0 ~ normal(9000, 2000);
  fq ~ normal(4500, 1000);
  noise ~ normal(0, 10000);
  w ~ beta(3,2);
  
  for (i in 1:N) {
    target += log_mix(w[i],
                      normal_lpdf(F[i] | F_temp[i], noise[1]),
                      normal_lpdf(F[i] | F_temp[i], noise[2]));
  }

}

generated quantities {
  real F_ppc[N];
  
  // Posterior predictive check
  for (i in 1:N) {
    if (uniform_rng(0.0, 1.0) < w[i]) {
      F_ppc[i] = normal_rng(F_temp[i], noise[1]);
    }
    else {
      F_ppc[i] = normal_rng(F_temp[i], noise[2]);
    }    
  }
}