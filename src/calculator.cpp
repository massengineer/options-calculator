#include <iostream>
#include <cmath>

using namespace std;


double cumulativeNormalDistribution(double x) {
    // Approximation of the cumulative normal distribution function
    
    // constants
    double a1 =  0.254829592;
    double a2 = -0.284496736;
    double a3 =  1.421413741;
    double a4 = -1.453152027;
    double a5 =  1.061405429;
    double p  =  0.3275911;

    // Save the sign of x
    int sign = 1;
    if (x < 0)
        sign = -1;
    x = fabs(x)/sqrt(2.0);

    // A&S formula 7.1.26
    double t = 1.0/(1.0 + p*x);
    double y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*exp(-x*x);

    return 0.5*(1.0 + sign*y);
}


void testCumulativeNormalDistribution() {
    // Select a few input values
    double x[] = {
        -3, 
        -1, 
        0.0, 
        0.5, 
        2.1 
    };

    // Output computed by Mathematica
    double y[] = { 
        0.00134989803163, 
        0.158655253931, 
        0.5, 
        0.691462461274, 
        0.982135579437 
    };

        int numTests = sizeof(x)/sizeof(double);

    double maxError = 0.0;
    for (int i = 0; i < numTests; ++i)
    {
        double error = fabs(y[i] - cumulativeNormalDistribution(x[i]));
        if (error > maxError)
            maxError = error;
    }

        cout << "Maximum error: " << maxError << "\n";
} 


pair<double, double> calculateD1D2(double S_null, double K, double r, double T, double sigma) {
    double d1 = (log(S_null / K) + (r + 0.5 * pow(sigma, 2)) * T) / (sigma * sqrt(T));
    double d2 = d1 - sigma * sqrt(T);
    return make_pair(d1, d2);
}


void testCalculateD1D2() {
    double S_null = 100.0; // Current stock price
    double K = 100.0;      // Strike price
    double r = 0.05;       // Risk-free interest rate
    double T = 1.0;        // Time to expiration in years
    double sigma = 0.2;    // Volatility

    auto [d1, d2] = calculateD1D2(S_null, K, r, T, sigma);
    cout << "d1: " << d1 << ", d2: " << d2 << "\n";
}


double calculateCallPrice(double S_null, double K, double r, double T, double sigma) {
    auto [d1, d2] = calculateD1D2(S_null, K, r, T, sigma);
    return S_null * cumulativeNormalDistribution(d1) - K * exp(-r * T) * cumulativeNormalDistribution(d2);
}


void testCalculateCallPrice() {
    double S_null = 100.0; // Current stock price
    double K = 100.0;      // Strike price
    double r = 0.05;       // Risk-free interest rate
    double T = 1.0;        // Time to expiration in years
    double sigma = 0.2;    // Volatility

    double callPrice = calculateCallPrice(S_null, K, r, T, sigma);
    cout << "Call Price: " << callPrice << "\n";
}


double calculatePutPrice(double S_null, double K, double r, double T, double sigma) {
    auto [d1, d2] = calculateD1D2(S_null, K, r, T, sigma);
    return K * exp(-r * T) * cumulativeNormalDistribution(-d2) - S_null * cumulativeNormalDistribution(-d1);
}


void testCalculatePutPrice() {
    double S_null = 100.0; // Current stock price
    double K = 100.0;      // Strike price
    double r = 0.05;       // Risk-free interest rate
    double T = 1.0;        // Time to expiration in years
    double sigma = 0.2;    // Volatility

    double putPrice = calculatePutPrice(S_null, K, r, T, sigma);
    cout << "Put Price: " << putPrice << "\n";
}


// int main() {
//     testCumulativeNormalDistribution();
//     testCalculateD1D2();
//     testCalculateCallPrice();
//     testCalculatePutPrice();
//     return 0;
// }