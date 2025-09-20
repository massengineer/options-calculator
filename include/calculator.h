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

// Function to calculate the normal probability density function
double normalProbabilityDensity(double x);

// Functions to calculate the Greeks for call options
double calculateDeltaCall(double S_null, double K, double r, double T, double sigma);
double calculateGammaCall(double S_null, double K, double r, double T, double sigma);
double calculateVegaCall(double S_null, double K, double r, double T, double sigma);
double calculateRhoCall(double S_null, double K, double r, double T, double sigma);
// Functions to calculate the Greeks for put options
double calculateDeltaPut(double S_null, double K, double r, double T, double sigma);
double calculateGammaPut(double S_null, double K, double r, double T, double sigma);
double calculateVegaPut(double S_null, double K, double r, double T, double sigma);
double calculateRhoPut(double S_null, double K, double r, double T, double sigma);

#endif // CALCULATOR_H