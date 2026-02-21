#include <stdlib.h>
#include <math.h>
#include <time.h>

double dWT()
{
    int num = 10;
    double dw = (rand() % (2*num + 1)) - num;
    return dw / 100.0;
}

double * VaR(double S, double drift, double volt, double t, int N)
{
    srand(time(NULL));
    double * value_at_risk = malloc(N*sizeof(double));
    int steps = 1776;
    double dt = t / (double)steps;

    for(int i = 0; i < N; ++i){
        double S0 = S;
        for(int j = 0; j < steps; ++j){
            S0 += drift*S0*dt + volt*S0*dWT();
        }
        double pct_change = S0 / S - 1.0;
        value_at_risk[i] = pct_change;
    }
    return value_at_risk;
}

void free_memory(double * x){
    free(x);
}