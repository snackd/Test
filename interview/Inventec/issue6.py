
"""
Issue6: 
1. 輸入 2 個 2 維矩陣 A 與 B
2. 輸出 2 矩陣相乘後 結果(C)
3. 再將 C 矩陣 反轉 列印
"""

def matrix_multiplication(A, B):
    if len(A[0]) != len(B):
        print("無法矩陣相乘： A 矩阵的 col != B 矩阵的 row")
        return None

    result = [[0] * len(B[0]) for _ in range(len(A))]

    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]

    return result

def transpose_matrix(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

def input_matrix(rows, cols):
    matrix = []
    print(f"请輸入 {rows} x {cols} 矩阵的元素：")

    while True:
        for i in range(rows):
            row = input(f"請輸入第 {i+1} row 的元素（用空格分隔）：").split()
            if len(row) != cols:
                print("row != cow，請重新輸入")
                matrix = []
                break
            matrix.append([int(num) for num in row])
        else:
            break
    return matrix

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))


# 統一使用原文，便於理解，因台灣為「直行橫列」，對岸則反過來
def main():
    rows_A = int(input("矩阵 A 的 row 數："))
    cols_A = int(input("矩阵 A 的 col 數："))
    print("矩阵 A：")
    A = input_matrix(rows_A, cols_A)

    rows_B = int(input("矩阵 B 的 row 數："))
    cols_B = int(input("矩阵 B 的 col 數："))
    print("矩阵 B：")
    B = input_matrix(rows_B, cols_B)

    if not A or not B:
        return

    print("矩阵 A：")
    print_matrix(A)
    print("矩阵 B：")
    print_matrix(B)

    result = matrix_multiplication(A, B)
    if result:
        print("AxB 矩阵结果：")
        print_matrix(result)

        transposed_result = transpose_matrix(result)
        print("轉置後：")
        print_matrix(transposed_result)

if __name__ == "__main__":
    main()
