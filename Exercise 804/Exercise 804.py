import time
import math

def solution( n ):  # works for square n only
    """
    >>> solution( 1_000_000 )
    492128
    >>> solution( 10**16 )
    4921370551019052

    >>> solution( 163_000_000 * 163_000_000 )  # requires isqrt
    13075589417108114
    """
    result = 0
    # m = round( math.sqrt(n) )
    m = math.isqrt( n - 1 ) + 1
    # for y in range( math.ceil( math.sqrt( 4 * n / 163 ) ) ):
    for y in range( math.isqrt( int( 4 * n / 163 ) - 1 ) + 1 ):
        """
        x**2 + x * y + 41 * y**2 <= n
        q = 41 * y**2 - n
        d = y**2 - 4 * q
        """
        # sqrt_d = math.sqrt( 4 * n - 163 * y**2 )
        sqrt_d = math.isqrt( 4 * n - 163 * y**2 ) + 0.5
        result += round( ( sqrt_d - y - 1 ) / 2 ) + round( ( sqrt_d + y - 1 ) / 2 ) + 1 
    return 2 * ( result - m - 1 )


# run the doctest cases:
print( ">>> doctest >>>" )
import doctest
doctest.testmod()
print( "<<< doctest <<<" )

start = time.perf_counter()
result = solution( 10**16 )
print( result, time.perf_counter() - start )  # 4921370551019052 17.8498841

# keep the window open:
input( "..." )  # activate/deactivate at will
