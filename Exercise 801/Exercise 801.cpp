#include <cstdio>
#include <cmath>
#include <algorithm>
#include <cassert>
#include <map>
#include <unordered_map>
const long long L=1e16,R=1e16+1e6;
const long long MOD=993353399;
const int UP=sqrt(R+0.5);
bool sieve[UP+100];
int primes[UP],top=0;
void init()
{
    for (int i=2;i<=UP;++i)
        if (!sieve[i])
        {
            primes[top++]=i;
            for (int j=i;j<=UP/i;++j)
                sieve[i*j]=true;
        }
}
long long powmod(long long x,long long y,long long mod)
{
    long long ret=1;
    for (x%=mod;y;y>>=1,x=x*x%mod)
        if (y&1) ret=ret*x%mod;
    return ret;
}
void decompose(long long n,std::unordered_map<long long,int> &li)
{
    for (int i=0;i<top && primes[i]<=n/primes[i];++i)
        for (;n%primes[i]==0;n/=primes[i],li[primes[i]]++);
    if (n>1) li[n]++;
}
int main()
{
    init();
    long long ans=0;
    #pragma omp parallel for reduction(+:ans) schedule(guided)
    for (long long i=std::max(2LL,L);i<=R;++i)
    {
        bool isprime=true;
        for (int j=0;j<top && primes[j]<=i/primes[j];++j)
            if (i%primes[j]==0)
            {
                isprime=false;
                break;
            }
        if (!isprime) continue;
        const long long moduli=i-1;
        std::unordered_map<long long,int> factors;
        decompose(moduli,factors);
        long long temp=1;
        for (const auto &j:factors)
        {
            long long p=j.first,e=j.second;
            temp=temp*((powmod(p,3*e,MOD)+powmod(p,3*e-1,MOD)-powmod(p,2*e-1,MOD))%MOD)%MOD;
        }
        temp=(temp+powmod(i-1,2,MOD))%MOD;
        if (i%10==1) printf("%lld: %lld\n",i,temp);
        ans+=temp;
    }
    printf("%lld\n",ans%MOD);
    return 0;
}
