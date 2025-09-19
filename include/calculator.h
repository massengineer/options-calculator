#ifndef CALCULATOR_H
#define CALCULATOR_H

#include <utility> // For std::pair
#include <cmath>   // For mathematical functions

// Function to approximate the cumulative normal distribution
double cumulativeNormalDistribution(double x);

// Function to calculate d1 and d2 for Black-Scholes formula
std::pair<double, double> calculateD1D2(double S_null, double K, double r, double T, double sigma);

// Function to calculate the price of a European call option
double calculateCallPrice(double S_null, double K, double r, double T, double sigma);

// Function to calculate the price of a European put option
double calculatePutPrice(double S_null, double K, double r, double T, double sigma);

// Test functions
void testCumulativeNormalDistribution();
void testCalculateD1D2();
void testCalculateCallPrice();
void testCalculatePutPrice();

#endif // CALCULATOR_H