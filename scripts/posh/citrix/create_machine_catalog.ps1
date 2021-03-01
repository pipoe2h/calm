# asnp citrix*
# Get-Command –Module Citrix.*

# Add-PSSnapin Citrix.*.Admin.V*

# $logop = Start-LogHighLevelOperation -AdminAddress "localhost" `
# -Source 'Studio' `
# -Text "Create Machine Catalog 'ExampleMachines'"

# New-BrokerCatalog -AdminAddress "localhost" `
# -AllocationType 'Permanent' `
# -Description 'Example Machines' `
# -IsRemotePC $False `
# -LoggingId $logop.Id `
# -MinimumFunctionalLevel 'L7' `
# -Name 'ExampleMachines' `
# -PersistUserChanges 'OnPvd' `
# -ProvisioningType 'MCS' `
# -Scope @() `
# -SessionSupport 'SingleSession'

$CTX_MACHINE_CATALOG_NAME = "@@{CTX_MACHINE_CATALOG_NAME}@@" # Machine Catalog name
$CTX_MACHINE_CATALOG_DESCRIPTION = "@@{CTX_MACHINE_CATALOG_DESCRIPTION}@@" # Description includes reference to "Managed by Calm"
$CTX_MACHINE_CATALOG_ALLOCATION = "@@{CTX_MACHINE_CATALOG_ALLOCATION}@@" # Random or Static (Random is default)
$CTX_MACHINE_CATALOG_PROVISIONING = "@@{CTX_MACHINE_CATALOG_PROVISIONING}@@" # MCS or PVS (only MCS for now)
$CTX_MACHINE_CATALOG_SESSION = "@@{CTX_MACHINE_CATALOG_SESSION}@@" # SingleSession or MultiSession (SingleSession is default)
$CTX_MACHINE_CATALOG_PERSISTUSER = "@@{CTX_MACHINE_CATALOG_PERSISTUSER}@@" # OnLocal, Discard or OnPvd (OnPvd is default and only applies if Allocation is static. If Random then Discard is only option)
$CTX_MACHINE_CATALOG_NAMING = "@@{CTX_MACHINE_CATALOG_NAMING}@@" # Example 'Machine-###'
$CTX_MACHINE_CATALOG_NAMING_TYPE = "@@{CTX_MACHINE_CATALOG_NAMING_TYPE}@@" # Numeric or Alphabetic (default Numeric)
$CTX_HOSTING_UNIT_PATH = "@@{CTX_HOSTING_UNIT_PATH}@@" # Customer to provide (Ex: XDHyp:\HostingUnits\NutanixResources - Can get the list using Get-Item XDHyp:\HostingUnits\*)
$CTX_MASTER_IMAGE_PATH = "@@{CTX_MASTER_IMAGE_PATH}@@" # XDHyp:\HostingUnits\SELab-Citrix-Desktops\WinSer2016_SysPrepped_Snap_Base_0.template
$MSFT_AD_CATALOG_OU = "@@{MSFT_AD_CATALOG_OU}@@"
$MSFT_AD_DOMAIN = "@@{MSFT_AD_DOMAIN}@@"
Add-PSSnapin Citrix.*.Admin.V*


#$brokerHypConnection = Get-BrokerHypervisorConnection
$hostingUnit = Get-Item $CTX_HOSTING_UNIT_PATH

# Start logged operation
$loggingOp = Start-LogHighLevelOperation -Source 'Calm' `
-Text "Create Machine Catalog '$CTX_MACHINE_CATALOG_NAME'"
$loggingId = $loggingOp.Id

# Create the broker catalog and the AD Identity account pool
$catalog = New-BrokerCatalog -Name $CTX_MACHINE_CATALOG_NAME `
-Description $CTX_MACHINE_CATALOG_DESCRIPTION `
-AllocationType $CTX_MACHINE_CATALOG_ALLOCATION `
-ProvisioningType $CTX_MACHINE_CATALOG_PROVISIONING `
-SessionSupport $CTX_MACHINE_CATALOG_SESSION `
-PersistUserChanges $CTX_MACHINE_CATALOG_PERSISTUSER `
-Scope @() `
-LoggingId $loggingId

$adPool = New-AcctIdentityPool -IdentityPoolName $CTX_MACHINE_CATALOG_NAME `
-NamingScheme $CTX_MACHINE_CATALOG_NAMING `
-NamingSchemeType $CTX_MACHINE_CATALOG_NAMING_TYPE `
-OU $MSFT_AD_CATALOG_OU `
-Domain $MSFT_AD_DOMAIN `
-AllowUnicode `
-LoggingId $loggingId

Set-BrokerCatalogMetadata -CatalogId $catalog.Uid `
-Name 'Citrix_DesktopStudio_IdentityPoolUid' `
-Value $adPool.IdentityPoolUid `
-LoggingId $loggingId
###################################################################
# Create the ProvisioningScheme and wait for it to complete (reporting progress)
$provSchemeTaskID = New-ProvScheme -ProvisioningSchemeName $CTX_MACHINE_CATALOG_NAME `
-HostingUnitUID $hostingUnit.HostingUnitUID `
-IdentityPoolUID $adPool.IdentityPoolUid `
-CleanOnBoot `
-MasterImageVM $CTX_MASTER_IMAGE_PATH `
-RunAsynchronously `
-LoggingId $loggingId

$provTask = Get-ProvTask -TaskID $provSchemeTaskID
$taskProgress = 0
Write-Host "Creating New ProvScheme"
while ($provTask.Active -eq $True)
{
    # catch an uninitialized task progress, this occurs until the product initialized the value
    try {
        $totalPercent = if ($provTask.TaskProgress){$provTask.TaskProgress} else {0}
    } catch {}
    Write-Progress -Activity "Creating Provisioning Scheme:" -Status "$totalPercent% Complete:" -PercentComplete $totalPercent
    sleep 30
    $provTask = Get-ProvTask -TaskID $provSchemeTaskID
}
Write-Host "New ProvScheme Creation Finished"
$provScheme = Get-ProvScheme -ProvisioningSchemeUID $provTask.ProvisioningSchemeUid
$controllers = Get-BrokerController | select DNSName
Add-ProvSchemeControllerAddress -ProvisioningSchemeUID $provScheme.ProvisioningSchemeUID `
-ControllerAddress $controllers `
-LoggingId $loggingId
###################################################################
# Set the provisioning scheme id for the broker catalog
Set-BrokerCatalog -InputObject $catalog `
-ProvisioningSchemeId $provTask.ProvisioningSchemeUid `
-LoggingId $loggingId
###################################################################