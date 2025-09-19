#include <iostream>
#include "../include/calculator.h"

using namespace std;

int main() {
  try {
    double S, K, r, T, sigma;

    cout << "Please enter the current stock price (S): ";
    cin >> S;
    if (S <= 0) {
        throw std::invalid_argument("Stock price must be positive.");
    }

    cout << "Please enter the strike price (K): ";
    cin >> K;
    if (K <= 0) {
        throw std::invalid_argument("Strike price must be positive.");
    }

    cout << "Please enter the risk-free interest rate (r) (as a decimal, e.g., 0.05 for 5%): ";
    cin >> r;
    if (r < 0) {
        throw std::invalid_argument("Interest rate cannot be negative.");
    }

    cout << "Please enter the time to expiration in years (T): ";
    cin >> T;
    if (T <= 0) {
        throw std::invalid_argument("Time to expiration must be positive.");
    }

    cout << "Please enter the volatility (sigma) (as a decimal, e.g., 0.2 for 20%): ";
    cin >> sigma;
    if (sigma <= 0) {
        throw std::invalid_argument("Volatility must be positive.");
    }

    cout << "Calculating option prices...\n";
    double callPrice = calculateCallPrice(S, K, r, T, sigma);
    double putPrice = calculatePutPrice(S, K, r, T, sigma);
    cout << "European Call Option Price: " << callPrice << "\n";
    cout << "European Put Option Price: " << putPrice << "\n";
  } catch(const std::invalid_argument& e) {
    std::cerr << "Error: Invalid input. " << e.what() << '\n';
  } catch(...) {
    std::cerr << "An unknown error occurred.\n";
  }
  
  return 0;
}