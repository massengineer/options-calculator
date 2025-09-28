// To be run without streamlit frontend implementation (this proves functionality of the C++ engine)

#include <iostream>
#include <stdexcept>
#include <limits>
#include "../include/calculator.h"

using namespace std;

int main() {
    try {
        double S, K, r, T, sigma;

        cout << "Please enter the current stock price (S): ";
        while (!(cin >> S) || S <= 0) {
            cout << "Invalid input. Stock price must be a positive number: ";
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        }

        cout << "Please enter the strike price (K): ";
        while (!(cin >> K) || K <= 0) {
            cout << "Invalid input. Strike price must be a positive number: ";
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        }
        
        cout << "Please enter the risk-free interest rate (r) (as a decimal, e.g., 0.05 for 5%): ";
        while (!(cin >> r) || r < 0) {
            cout << "Invalid input. Interest rate cannot be a negative number: ";
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        }

        cout << "Please enter the time to expiration in years (T): ";
        while (!(cin >> T) || T <= 0) {
            cout << "Invalid input. Time to expiration must be a positive number: ";
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        }
        
        cout << "Please enter the volatility (sigma) (as a decimal, e.g., 0.2 for 20%): ";
        while (!(cin >> sigma) || sigma <= 0) {
            cout << "Invalid input. Volatility must be a positive number: ";
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        }
        
        cout << "Calculating option prices...\n";
        double callPrice = calculateCallPrice(S, K, r, T, sigma);
        double putPrice = calculatePutPrice(S, K, r, T, sigma);
        cout << "European Call Option Price: " << callPrice << "\n";
        cout << "European Put Option Price: " << putPrice << "\n";
    
    } catch(const invalid_argument& e) {
        cerr << "Error: Invalid input. " << e.what() << '\n';
    } catch(...) {
        cerr << "An unknown error occurred.\n";
    }

    return 0;
}