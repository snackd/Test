import math

"""
Issue3: 
1. 判斷 2 圓之間 「距離」
2. 根據 Reference 的公式，判斷 2 圓之間關係
"""

# Reference: https://www.liveism.com/live-concept.php?q=%E5%85%A9%E5%9C%93%E7%9A%84%E4%BD%8D%E7%BD%AE%E9%97%9C%E4%BF%82

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def circleRelation(x1, y1, r1, x2, y2, r2):
    dist = distance(x1, y1, x2, y2)
    print("2 圓心距離：", dist)
    if r1 == r2:
        if dist == 0:
            print("重合(完全重合)")
        elif dist < r1:
            print("內離(相交於 1 點)，圓內含於另 1 圓")
        elif dist == r1:
            print("內切(相交於 1 點)，圓內含於另 1 圓")
        else:
            print("內離(不相交)，圓外含於另一圓")
    elif dist < abs(r1 - r2):
        if r1 < r2:
            print("內離(不相交)，第 1 個圓在第 2 個圓內部，2 圓重疊")
        else:
            print("內離(不相交)，第 2 個圓在第 1 個圓內部，2 圓重疊")
    elif dist < (r1 + r2):
        print("相交(相交於 2 點)，2 圓重疊")
    elif dist == abs(r1 - r2):
        print("內切(相交於 1 點)")
    elif dist == (r1 + r2):
        print("外切(相交於 1 點)")
    else:
        # dist > (r1 + r2)
        print("外離(不相交)，2 圓無相交")
        
# 第 1 個圓 
x1 = float(input("第 1 個圓中心 x 座標："))
y1 = float(input("第 1 個圓中心 y 座標："))
r1 = float(input("第 1 個圓半徑 r："))

# 第 2 個圓
x2 = float(input("第 2 個圓中心 x 座標："))
y2 = float(input("第 2 個圓中心 y 座標："))
r2 = float(input("第 2 個圓半徑 r："))

relation = circleRelation(x1, y1, r1, x2, y2, r2)