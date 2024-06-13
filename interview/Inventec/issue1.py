import re

"""
Issue1: 將輸入
1. 判斷是否字串
2. 判斷是否可轉數字 (dec)
3. 將 dec 轉 bin
4. 判斷 bin 中有幾個 1
"""

MAX_INT = pow(2, 31) - 1  
MIN_INT = - pow(2, 31)
MAX_LENGTH = len(str(MAX_INT)) + 1  # 設置最大輸入長度, 10 (可輸入負為 11)

def limitInput(value) -> int:

    while True:
        inputStr = input(value)

        if len(inputStr) > MAX_LENGTH:
            print("輸入的字串長度不能超過", MAX_LENGTH, "個字符。請重新輸入。")
            continue

        # if not isString(inputStr):
        #     print("非字串")
        #     continue

        if not isNumericString(inputStr):
            print("輸入的字串包含非數字字符。請輸入只包含0-9正負整數字串。")
            continue

        inputValue = int(inputStr)
        if not (MIN_INT <= int(inputValue) <= MAX_INT):
            print("超過 INT 上限數:", MAX_INT)
            continue

        return inputValue

# def isString(inputStr:str) -> bool:
#     return isinstance(inputStr, str)

def isNumericString(inputStr:str) -> bool:
    return bool(re.match(r'^-?\d+$', inputStr))

def decimalToBinary(value:int) -> int:
    # print(bin(value))
    # 濾掉 0b
    return bin(value)[2:]

def oriDecimalToBinary(value:int) -> str:
    binStr = ""

    if value == 0:
        return '0'
    
    # 2’s Complement
    if value < 0:
        value = 2**32 + value  
    else:
        value = value
    
    while value > 0:
        binStr = str(value % 2) + binStr
        value = value // 2

    return binStr


def oriBinaryCountOne(binStr:str) -> int:
    count = 0

    for char in binStr:
        if char == '1':
            count += 1

    return count 

def binaryCountOne(binStr:str) -> int:
    return binStr.count('1')

def main():
    value = limitInput("輸入: ")

    # binValue = decimalToBinary(value)
    binValue = oriDecimalToBinary(value)
    print("轉為 bin:", binValue)

    # count = binaryCountOne(binValue)
    count = oriBinaryCountOne(binValue)
    print("總共有", count ,"個 1")


if __name__ == "__main__":
    main()