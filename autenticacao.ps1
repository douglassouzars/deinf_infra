Param(
    [Parameter(Mandatory=$true)]
    [string]$Username,

    [Parameter(Mandatory=$true)]
    [string]$Password
)

# Carrega o módulo ActiveDirectory
Import-Module ActiveDirectory

# Tenta autenticar o usuário no Active Directory
$Credential = New-Object System.Management.Automation.PSCredential ($Username, (ConvertTo-SecureString -String $Password -AsPlainText -Force))
$Authenticated = $false
Try {
    $ADUser = Get-ADUser -Identity $Username -Server "NOVACAP.SEDE" -Credential $Credential
    $Authenticated = $true
} Catch {
    $Authenticated = $false
}

# Retorna o resultado da autenticação
If ($Authenticated) {
    Write-Output "User authenticated successfully"
} Else {
    Write-Output "User authentication failed"
}
