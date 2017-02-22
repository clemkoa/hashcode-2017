
#include <iostream>
#include <fstream>
#include <string>

#include <vector>

#include "localsolver.h"
#include "libs.h"

using namespace localsolver;
using namespace std;

class Callback : public LSCallback {
  int objective;
public:
  void callback(LocalSolver& solver, LSCallbackType type);
};

class Model {

  // Problem parameters
  // int n;

  // Decision variables
  // vector<LSExpression> x; 

  // Intermediate expressions

  // Objective expression
  LSExpression objective;

  // Run code during search
  Callback cb;

  // Solver
  LocalSolver ls;

public:
  void readData(const string& fileName);

  void defineModel();
  void solve(int timeLimit);

  void printSolution();

private:
  void declareVariables(LSModel &model);
  void declareIntermediate(LSModel &model);
  void declareConstraints(LSModel &model);
  void declareObjective(LSModel &model);
};

class Callback : public LSCallback {
public:
  void callback(LocalSolver& solver, LSCallbackType type) {
    Log::Verbose("OK");
  }
};
