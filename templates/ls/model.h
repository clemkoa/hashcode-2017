
#include <iostream>
#include <fstream>
#include <string>

#include <vector>

#include "localsolver.h"
#include "libs.h"

using namespace localsolver;
using namespace std;

using Int = unsigned int;

class Model {

  // Problem parameters
  // Int n;

  // Decision variables
  // vector<LSExpression> x; 

  // Intermediate expressions

  // Objective expression
  LSExpression objective;

  // Solver
  LocalSolver ls;

public:
  void readData(const string& fileName, Int nSlicesOverride);

  void defineModel();
  void solve(Int timeLimit);

  void printSolution();

private:
  void declareVariables(LSModel &model);
  void declareIntermediate(LSModel &model);
  void declareConstraints(LSModel &model);
  void declareObjective(LSModel &model);
};
