#include <cmath>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>

using namespace std;

constexpr int NUM_PATIENTS = 1000000;

int random_int(int min, int max) { return rand() % (max - min + 1) + min; }

float random_float(float min, float max) {
  return min + static_cast<float>(rand()) /
                   (static_cast<float>(RAND_MAX / (max - min)));
}

int main(int argc, char **argv) {
  srand(time(NULL));

  int N = pow(10, std::stoi(argv[1]));
  vector<int> ids;
  ids.reserve(N);
  vector<int> timestamps(N);
  timestamps.reserve(N);
  vector<int> patient_ids(N);
  patient_ids.reserve(N);
  vector<float> spo2s(N);
  spo2s.reserve(N);
  vector<float> hrs(N);
  hrs.reserve(N);
  vector<float> bps(N);
  bps.reserve(N);
  for (int i = 0; i < N; i++) {
    ids.push_back(i);
    timestamps.push_back(random_int(0, 1000000));
    patient_ids.push_back(random_int(0, NUM_PATIENTS));
    spo2s.push_back(random_float(95.0f, 100.0f));
    hrs.push_back(random_float(60.0f, 100.0f));
    bps.push_back(random_float(100.0f, 140.0f));
  }
  ofstream out;
  out.open("output.txt");
  out << "id,timestamp,patient_id,spo2,hr,bp\n";
  for (int i = 0; i < N; i++) {
    out << ids[i] << "," << timestamps[i] << "," << patient_ids[i] << ","
        << spo2s[i] << "," << hrs[i] << "," << bps[i] << endl;
  }
}