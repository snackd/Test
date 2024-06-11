' 創建FileSystemObject對象
Set objFSO = CreateObject("Scripting.FileSystemObject")

' 獲取當前日期，並格式化為YYYYMMDD
strYear = Year(Date)
strMonth = Right("0" & Month(Date), 2)
strDay = Right("0" & Day(Date), 2)

' 設置年度文件夾路徑
strYearFolderPath = "C:\Work\Test\" & strYear
' 設置月度文件夾路徑
strMonthFolderPath = strYearFolderPath & "\" & strMonth
' 設置每日文件夾路徑
strDateFolderPath = strMonthFolderPath & "\" & strDay

' 檢查並創建年度文件夾
If Not objFSO.FolderExists(strYearFolderPath) Then
    On Error Resume Next
    objFSO.CreateFolder strYearFolderPath
    If Err.Number <> 0 Then
        WScript.Echo "創建年度文件夾時出錯: " & Err.Description
        On Error GoTo 0
        WScript.Quit 1
    End If
    On Error GoTo 0
End If

' 檢查並創建月度文件夾
If Not objFSO.FolderExists(strMonthFolderPath) Then
    On Error Resume Next
    objFSO.CreateFolder strMonthFolderPath
    If Err.Number <> 0 Then
        WScript.Echo "創建月度文件夾時出錯: " & Err.Description
        On Error GoTo 0
        WScript.Quit 1
    End If
    On Error GoTo 0
End If

' 檢查並創建每日文件夾
If Not objFSO.FolderExists(strDateFolderPath) Then
    On Error Resume Next
    objFSO.CreateFolder strDateFolderPath
    If Err.Number <> 0 Then
        WScript.Echo "創建每日文件夾時出錯: " & Err.Description
        On Error GoTo 0
        WScript.Quit 1
    End If
    On Error GoTo 0
End If
