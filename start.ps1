

# �� PowerShell ������ʽ����Ϊ����
Add-Type -TypeDefinition @"
    using System;
    using System.Runtime.InteropServices;
    public class WinAPI
    {
        [DllImport("user32.dll")]
        public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
        [DllImport("kernel32.dll")]
        public static extern IntPtr GetConsoleWindow();
        public const int SW_HIDE = 0;
    }
"@

$consolePtr = [WinAPI]::GetConsoleWindow()
[WinAPI]::ShowWindow($consolePtr, [WinAPI]::SW_HIDE)

chcp 936
cd .\project
py MainWindow.py