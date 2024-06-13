import math

"""
Issue2: 
1. 判斷 1 數是否為質數
2. 範圍為 2-100
"""

def isPrime(n: int) -> bool:

    if n <= 1:
        return False

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    #  16 = 4, 25 = 5, 36 = 6
    sqrtN = int(math.sqrt(n))

    # O(sqrt(n)/2)
    # 只檢索奇數: 3, 5, 7 
    for i in range(3, sqrtN + 1, 2):
        if n % i == 0:
            return False
    return True

print("2 到 100 所有質數：")
for num in range(2, 101):
    if isPrime(num):
        print(num, end=" ")
