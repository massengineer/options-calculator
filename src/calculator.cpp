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


pair<double, double> calculateD1D2(double S_null, double K, double r, double T, double sigma) {
    double d1 = (log(S_null / K) + (r + 0.5 * pow(sigma, 2)) * T) / (sigma * sqrt(T));
    double d2 = d1 - sigma * sqrt(T);
    return make_pair(d1, d2);
}


double calculateCallPrice(double S_null, double K, double r, double T, double sigma) {
    auto [d1, d2] = calculateD1D2(S_null, K, r, T, sigma);
    return S_null * cumulativeNormalDistribution(d1) - K * exp(-r * T) * cumulativeNormalDistribution(d2);
}


double calculatePutPrice(double S_null, double K, double r, double T, double sigma) {
    auto [d1, d2] = calculateD1D2(S_null, K, r, T, sigma);
    return K * exp(-r * T) * cumulativeNormalDistribution(-d2) - S_null * cumulativeNormalDistribution(-d1);
}


double normalProbabilityDensity(double x) {
    return (1.0 / sqrt(2 * M_PI)) * exp(-0.5 * pow(x, 2));
}


// Calculating greeks
double calculateDeltaCall(double S_null, double K, double r, double T, double sigma) {
    auto [d1, d2] = calculateD1D2(S_null, K, r, T, sigma);
    return cumulativeNormalDistribution(d1);
}


double calculateDeltaPut(double S_null, double K, double r, double T, double sigma) {
    auto [d1, d2] = calculateD1D2(S_null, K, r, T, sigma);
    return cumulativeNormalDistribution(d1) - 1;
}


double calculateGammaInternalHelper(double S_null, double K, double r, double T, double sigma) {
    auto [d1, d2] = calculateD1D2(S_null, K, r, T, sigma);
    return normalProbabilityDensity(d1) / (S_null * sigma * sqrt(T));
}


double calculateGammaCall(double S_null, double K, double r, double T, double sigma) {
    return calculateGammaInternalHelper(S_null, K, r, T, sigma);
}


double calculateGammaPut(double S_null, double K, double r, double T, double sigma) {
    return calculateGammaInternalHelper(S_null, K, r, T, sigma);
}


double calculateVegaInternalHelper(double S_null, double K, double r, double T, double sigma) {
    auto [d1, d2] = calculateD1D2(S_null, K, r, T, sigma);
    return S_null * normalProbabilityDensity(d1) * sqrt(T);
}


double calculateVegaCall(double S_null, double K, double r, double T, double sigma) {
    return calculateVegaInternalHelper(S_null, K, r, T, sigma);
}


double calculateVegaPut(double S_null, double K, double r, double T, double sigma) {
    return calculateVegaInternalHelper(S_null, K, r, T, sigma);
}


double calculateThetaCall(double S_null, double K, double r, double T, double sigma) {
    auto [d1, d2] = calculateD1D2(S_null, K, r, T, sigma);
    double term1 = - (S_null * normalProbabilityDensity(d1) * sigma) / (2 * sqrt(T));
    double term2 = r * K * exp(-r * T) * cumulativeNormalDistribution(d2);
    return term1 - term2;
}


double calculateThetaPut(double S_null, double K, double r, double T, double sigma) {
    auto [d1, d2] = calculateD1D2(S_null, K, r, T, sigma);
    double term1 = - (S_null * normalProbabilityDensity(d1) * sigma) / (2 * sqrt(T));
    double term2 = r * K * exp(-r * T) * cumulativeNormalDistribution(-d2);
    return term1 + term2;
}


double calculateRhoCall(double S_null, double K, double r, double T, double sigma) {
    auto [d1, d2] = calculateD1D2(S_null, K, r, T, sigma);
    return K * T * exp(-r * T) * cumulativeNormalDistribution(d2);
}


double calculateRhoPut(double S_null, double K, double r, double T, double sigma) {
    auto [d1, d2] = calculateD1D2(S_null, K, r, T, sigma);
    return -K * T * exp(-r * T) * cumulativeNormalDistribution(-d2);
}
