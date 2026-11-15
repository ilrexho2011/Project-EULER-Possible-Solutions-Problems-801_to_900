#include <iostream>
#include <deque>
using namespace std;

void PureFactors(long long mod)
{
	deque<long long> pureFacList = {};
	pureFacList.push_back(2);
	long long allFac = 1;
	long long total = 2;
	for (int i = 1; i < 1e7; ++i) 
	{
		 allFac *= 2;
		 allFac %= mod;
		 long long fac = allFac;
		 for (int j = 1; j <= sqrt(i + 1); ++j)
		 {
			 if ((i + 1) % j == 0) 
			 {
				 fac -= pureFacList[j - 1];
				 fac %= mod;
				 if (j != (i + 1) / j && j != 1)
				 {
					 fac -= pureFacList[(i + 1) / j - 1];
					 fac %= mod;
				 }
			 }
		 }
		 pureFacList.push_back(fac);
		 total += fac;
		 total %= mod;
	}
	if (total < 0)
		total += mod;
	cout << total << "\n";
}

int main()
{
	PureFactors(1020340567);
}
