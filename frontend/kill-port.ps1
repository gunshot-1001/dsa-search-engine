$port = 5174
$connection = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue

if ($connection) {
    $procId = ($connection | Select-Object -First 1).OwningProcess
    if ($procId -and $procId -ne 0) {
        Write-Output "Killing process on port $port (PID $procId)..."
        Stop-Process -Id $procId -Force
    } else {
        Write-Output "⚠️ Found PID $procId (system process), skipping..."
    }
} else {
    Write-Output "No process found on port $port."
}
