#include <stdio.h>

//#define FIND_A0
//#define FIND_COEFFS

int main()
{
#if defined(FIND_A0)
	//const char prefix[] = "EULERcats";
	const char prefix[] = "PuzzleOne";
	//const char prefix[] = "LuckyText";
#define PREFIXLEN (sizeof(prefix)-1)
	unsigned data[PREFIXLEN];
	int i, j;
	for (i = 0; i < PREFIXLEN; i++)
		data[i] = (prefix[i] < 'a' ? prefix[i] - 'A' + 26 : prefix[i] - 'a');
	for (int low = 0; low < 65536; low++) {
		unsigned a0low = ((data[0] % 4) << 16) + low;
		unsigned cur = a0low;
		for (i = 0; i < PREFIXLEN; i++) {
			if ((cur >> 16) % 4 != data[i] % 4)
				break;
			cur = cur * (unsigned)(25214903917LL % (1 << 18)) + 11;
		}
		if (i == PREFIXLEN) {
			for (unsigned long long a0 = (data[0] << 16) + low; a0 < (1ULL << 48); a0 += 52 << 16) {
				unsigned long long cur = a0;
				for (i = 0; i < PREFIXLEN; i++) {
					if ((cur >> 16) % 52 != data[i])
						break;
					cur = (cur * 25214903917ULL + 11) % (1ULL << 48);
				}
				if (i == PREFIXLEN) {
					printf("found a0: %llu\n", a0);
				}
			}
		}
	}
#elif defined(FIND_COEFFS)
	unsigned long long d0 = 0, d1 = 1;
	int i;
	for (i = 0; i < (1 << 24); i++) {
		d0 = (d0 * 25214903917ULL + 11) % (1ULL << 48);
		d1 = (d1 * 25214903917ULL + 11) % (1ULL << 48);
	}
	printf("%llu*x + %llu\n", d1 - d0, d0);
#else
	unsigned long long source = 144933752257087ULL;
	unsigned long long target = 160163661474491ULL;
	unsigned long long attempts = 0;
	int i;
	for (i = 0; (source - target) % (1ULL << 24); i++) {
		source = (source * 25214903917ULL + 11) % (1ULL << 48);
		++attempts;
	}
	// repeat 2**24 times: 122971960115201 * x + 30583270932480
	for (i = 0; source != target; i++) {
		source = (source * 122971960115201ULL + 30583270932480) % (1ULL << 48);
		attempts += 1 << 24;
	}
	printf("%llu\n", attempts);
#endif
	return 0;
}
