
#include "model.h"

// ------------------------------- Data Functions ------------------------------

void Model::readData(const string& fileName) {
  Timed timed("Reading problem data");
}

// ------------------------------- Model Functions -----------------------------

void Model::defineModel() {
  Timed timed("Defining model");

  LSModel model = ls.getModel();
  ls.addCallback(CT_TimeTicked, &cb);

  // Declare all LSExpressions
  declareVariables(model);
  declareIntermediate(model);

  declareConstraints(model);
  declareObjective(model);

  Log::Info("");
  model.close();
}

void Model::declareVariables(LSModel &model) {
  Timed timed("Declaring decision variables", Log::Level::DEBUG);
  
  // x.resize(n);

  // for (unsigned int i = 0 ; i < n ; i++)
  //   // Use boolVar, intVar or floatVar
  //   x[i] = model.intVar(0, K); // [min, max]  
}

void Model::declareIntermediate(LSModel &model) {
  Timed timed("Declaring intermediate expressions", Log::Level::DEBUG);

  // LSExpression sum = model.sum();
  // for (unsigned int i = 0 ; i < n ; i++)
  //   sum += x[i];

  // LSExpression a = sum + static_cast<lsint>(5);

  // // Data array to be accessed by decision variable index
  // LSExpression array = model.array(data.begin(), data.end());
  // LSExpression intermediate = model.at(array, x);
}

void Model::declareConstraints(LSModel &model) {
  Timed timed("Declaring constraints", Log::Level::DEBUG);

  // {
  //   Timed timed("First constraint", Log::Level::VERBOSE);
  //   for (unsigned int i = 0 ; i < n ; i++)
  //     model.constraint((x[i] >= 5) || (x[i] == 0));
  // }
}

void Model::declareObjective(LSModel &model) {
  objective = model.sum();
  for (unsigned int i = 0 ; i < n ; i++)
    objective += x[i];

  model.maximize(objective);
}

void Model::solve(int timeLimit) {  
  // Parameterizes the solver
  LSPhase phase = ls.createPhase();
  phase.setTimeLimit(timeLimit);

  // Check your model runs fine first then try with 4 threads
  // ls.getParam().setNbThreads(4);

  ls.solve();
}

// ------------------------------- Utils Functions -----------------------------

void Model::printSolution() {
  cout << endl;

  cout << "Objective: " << objective.getValue();
}

// ----------------------------- Callback Function -----------------------------

void Callback::callback(LocalSolver& solver, LSCallbackType type) {
  // int newObjective = ls.getModel().getObjective(0);
  // if (newObjective > objective) {
  //   objective = newObjective;

  //   writeSolution();
    
  //   Log::Verbose("Wrote solution with objective = " + to_string(objective));
  // }
}

// ------------------------------- Main Functions ------------------------------

int main(int argc, char* argv[]) {
  if (argc < 3)
    Log::Error("Syntax: ./model fileName timeLimit");

  const string fileName(argv[1]);
  const int timeLimit = stoi(argv[2]);

  Model model;

  model.readData(fileName);

  model.defineModel();
  model.solve(timeLimit);

  model.printSolution();

  return EXIT_SUCCESS;
}
