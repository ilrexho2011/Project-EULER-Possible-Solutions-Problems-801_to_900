#include <bits/stdc++.h>

int64_t T_ellipse(int64_t N) {
	int64_t ans = 0;
	// number of points of the form x^2 + 163 y^2 <= 4N with x == y mod 2
	for (int64_t y = 0, x = 0; 163 * y * y <= 4 * N; y++) {
		if (y == 0) {
			while ((x+1) * (x+1) <= 4 * N - 163 * y * y) x++;
		} else {
			while (x * x > 4 * N - 163 * y * y) x--;
		}
		int64_t ways = (y & 1) ? (x+1) / 2 * 2 : x / 2 * 2 + 1;
		ans += (y == 0 ? 1 : 2) * ways;
	}
	ans--;
	return ans;
}

int64_t T_quadratic_field(int64_t N) {
	// Compute the prefix sums of the Legendre symbol
	std::array<int, 163> val; val.fill(-1);
	val[0] = 0;
	for (int i = 1; 2*i <= 163; i++) val[i*i%163] = 1;

	for (int i = 1; i < 163; i++) val[i] += val[i-1];

	int64_t ans = 0;
	for (int64_t x = 1; x <= N; x++) {
		int64_t nx = N / (N / x);
		ans += val[(N / x) % 163] * (nx - x + 1);
		x = nx;
	}
	return ans * 2;
}

int64_t T(int64_t N) {
	//return T_ellipse(N);
	return T_quadratic_field(N);
}

int main() {
	using namespace std;
	ios_base::sync_with_stdio(false), cin.tie(nullptr);

	cerr << T(1e3) << '\n';
	cerr << T(1e6) << '\n';
	cout << T(1e16) << '\n';

	return 0;
}
