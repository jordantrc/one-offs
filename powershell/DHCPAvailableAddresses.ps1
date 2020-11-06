Param (
    [string]$Scope = "",
    [string]$Server = ""
)

$scopeString = $scope + "0"

write-host "Checking for available address in the" $scopeString "DHCP scope"

$validAddresses = @()
for($i = 2; $i -le 254; $i++) {
    $num = [string]$i
    $validAddresses += $scope + $num
}

$serverString = "\\" + $Server

$ipAddresses = @()
netsh dhcp server $serverString scope $scopeString show clientsvq | foreach {
    $ip_address = ($_ -split '\s+-')[0]
    if($ip_address -match '^\d+\.\d+\.\d+\.\d+') 
    {
        $ipAddresses += $ip_address
    }
}

# check the valid addresses against the reservations
$i = 1
Write-Host "Available addresses:"
foreach($addr In $validAddresses) {
    if($ipAddresses -notcontains $addr){
        write-host $i "-" $addr
        $i++
    }
}