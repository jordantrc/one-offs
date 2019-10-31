Param (
    [string]$Computer = 'localhost',
    [Int32]$Delay = 60
    )

Write-Host "Testing connectivity to" $Computer "every" $Delay "seconds"
Write-Host "Date            Response Time (ms)"

while(1) {
    $results = test-connection -ComputerName $Computer -Count 2
    $date = get-date -format 'T'
    Write-Host $date "          " $results[0].Properties['ResponseTime'].Value
    sleep -s $Delay
}