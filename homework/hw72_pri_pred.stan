data {
  int N;  
  real a;
  real b;
  int Nt;
}

generated quantities{
  real n[N];
  real theta = beta_rng(a, b);
  
  for (i in 1:N) {
    n[i] = binomial_rng(Nt, theta);
  }
}