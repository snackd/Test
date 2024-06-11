"""
Issue5: 
1. N 個人圍成一圈並順序排號
2. 從第 1 個人開始報數, 1, 2, 3 等順序, 每報到 3 的人退出
3. 最後留下編號的會是幾？
"""


# 約瑟夫環 (LinkList)

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

def josephus(n, step):
    head = Node(1)
    current = head
    for i in range(2, n + 1):
        current.next = Node(i)
        current = current.next

    # 閉合環
    current.next = head  

    # 模擬：報數移除節點
    current = head
    while current.next != current:
        # 跳過當前節點 的 前 2 個節點
        for _ in range(step - 1):
            prev = current
            current = current.next
        # 移除當前節點
        prev.next = current.next
        current = prev.next

    return current.value

n = 10
step = 3
winner = josephus(n, step)
print("最後留下的編號是:", winner)

