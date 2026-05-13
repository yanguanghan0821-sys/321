@echo off
REM 关闭HDR
powershell -Command "Add-Type -AssemblyName System.Runtime.WindowsRuntime; try { $s=[Windows.Media.Display.HdrDisplay]::GetStatusAsync().GetAwaiter().GetResult(); if($s.Active){[Windows.Media.Display.HdrDisplay]::SetHdrEnabledAsync($false).GetAwaiter().GetResult(); echo HDR已关闭} else { echo HDR已经是关闭状态} } catch { echo HDR操作失败; reg add HKCU\Software\Microsoft\DirectX\UserGpuPreferences /v HdrEnabled /t REG_DWORD /d 0 /f 2>nul; echo HDR已强制关闭(注册表) }"

REM 关闭G-Sync - 通过NVIDIA注册表
reg add "HKLM\SOFTWARE\NVIDIA Corporation\Global\NVTweak" /v "GSyncEnabled" /t REG_DWORD /d 0 /f 2>nul
reg add "HKCU\SOFTWARE\NVIDIA Corporation\Global\NVTweak" /v "GSyncEnabled" /t REG_DWORD /d 0 /f 2>nul
reg add "HKLM\SOFTWARE\NVIDIA Corporation\Global\NVTweak" /v "GSyncFeatureOverride" /t REG_DWORD /d 0 /f 2>nul
reg add "HKLM\SYSTEM\CurrentControlSet\Control\NVIDIA\Global\NVTweak" /v "GSyncEnabled" /t REG_DWORD /d 0 /f 2>nul
echo G-Sync 已关闭

REM 电源模式设为最高性能
reg add "HKLM\SOFTWARE\NVIDIA Corporation\Global\NVTweak" /v "PowerMizerEnable" /t REG_DWORD /d 0 /f 2>nul
reg add "HKLM\SOFTWARE\NVIDIA Corporation\Global\NVTweak" /v "PrefPowerMode" /t REG_DWORD /d 1 /f 2>nul
echo 电源模式已设为最高性能

echo.
echo 全部设置完成！建议重启电脑生效。
pause
