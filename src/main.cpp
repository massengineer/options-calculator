#include <iostream>
#include "../include/calculator.h"

using namespace std;

int main() {
  cout << "Please enter the current stock price (S): ";
  double S;
  cin >> S;
  cout << "Please enter the strike price (K): ";
  double K;
  cin >> K;
  cout << "Please enter the risk-free interest rate (r) (as a decimal, e.g., 0.05 for 5%): ";
  double r;
  cin >> r;
  cout << "Please enter the time to expiration in years (T): ";
  double T;
  cin >> T;
  cout << "Please enter the volatility (sigma) (as a decimal, e.g., 0.2 for 20%): ";
  double sigma;
  cin >> sigma;
  cout << "Calculating option prices...\n";
  double callPrice = calculateCallPrice(S, K, r, T, sigma);
  double putPrice = calculatePutPrice(S, K, r, T, sigma);
  cout << "European Call Option Price: " << callPrice << "\n";
  cout << "European Put Option Price: " << putPrice << "\n";
  return 0;
}