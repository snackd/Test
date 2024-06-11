"""
Issue4: 
1. 將字段反轉輸出
"""

def reverse_words(s: str) -> str:
    # 使用 s.split 以空白(space) 切出字段
    words = s.split()  

    # 使用 list 反輸出，達到逆轉字段功用
    reversed_words = [word[::-1] for word in words]  
    return ' '.join(reversed_words)  

s = "Let's take LeetCode contest"
result = reverse_words(s)
print(result)
