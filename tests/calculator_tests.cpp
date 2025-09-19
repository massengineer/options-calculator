#include <iostream>
#include <cmath>
#include "../include/calculator.h"

using namespace std;


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


void testCalculateD1D2() {
    double S_null = 100.0; // Current stock price
    double K = 100.0;      // Strike price
    double r = 0.05;       // Risk-free interest rate
    double T = 1.0;        // Time to expiration in years
    double sigma = 0.2;    // Volatility

    auto [d1, d2] = calculateD1D2(S_null, K, r, T, sigma);
    cout << "d1: " << d1 << ", d2: " << d2 << "\n";
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


void testCalculatePutPrice() {
    double S_null = 100.0; // Current stock price
    double K = 100.0;      // Strike price
    double r = 0.05;       // Risk-free interest rate
    double T = 1.0;        // Time to expiration in years
    double sigma = 0.2;    // Volatility

    double putPrice = calculatePutPrice(S_null, K, r, T, sigma);
    cout << "Put Price: " << putPrice << "\n";
}


int main() {
    testCumulativeNormalDistribution();
    testCalculateD1D2();
    testCalculateCallPrice();
    testCalculatePutPrice();
    return 0;
}