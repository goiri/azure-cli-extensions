# Azure Bastion behind Azure Front Door
For some reason (security!?), accessing Azure Bastion from external IPs is not secure.
However, putting the Azure Bastion behind Azure Front Door makes everybody happy; sure.

The problem is that the `az cli` expects to connect directly to the Azure Bastion.
This hacky extension overwrites the Azure Bastion address with the Azure Front Door address.
It also ignores the mismatch of host names in the SSL handshake.

Note that this requires an Azure Front Door setup pointing to the Azure Bastion IP.

## Install the extension
We clone the Bastion subtree of the remote repository, compile the extension, remove the previous version, and install the new one:
```bash
git clone --filter=blob:none --no-checkout https://github.com/goiri/azure-cli-extensions.git
cd azure-cli-extensions
git sparse-checkout init --cone
git sparse-checkout set src/bastion
git checkout main

cd src\bastion
pip install --upgrade setuptools wheel
python setup.py bdist_wheel
az extension remove -n bastion
az extension add --source .\dist\bastion-1.4.0-py3-none-any.whl
```


## Create Azure Front Door
One needs to create an Azure Front Door that points to the "public" DNS/IP of the Azure Bastion.

Some example bicep script to create a full setup with VMSS, Bastion, and Front Door can be found [here](https://dev.azure.com/azsr/AzureDeploy/_git/AzTemplates/pullrequest/292).
Based on that, to deploy all the components:
```powershell
az bicep generate-params --file .\vmss-linux-frontdoor-bastion.bicep --output-format bicepparam --include-params all
# Tune the vmss-linux-frontdoor-bastion.bicepparam file

$RESOURCE_GROUP="<choose>"
$REGION="<choose>"
az group create --name $RESOURCE_GROUP --location $REGION
az deployment group create --resource-group $RESOURCE_GROUP --parameters .\vmss-linux-frontdoor-bastion.bicepparam
```

Note that this creation takes a long time (>5 minutes) because we need to wait for the Bastion to be created and then the Front Door.
On top of this, the Azure Front Door will also take some time to detect the Bastion IP.

## Use the extension
Now, one can pass the Azure Front Door address with the `--frontdoor` argument:
```bash
az network bastion ssh --name <bastion-name> -g <resource-group> --target-ip-address <local-vm-ip> --auth-type "password" --username azureuser --frontdoor <frontdoor-address>
```

There is another option to let the extension auto-detect the Azure Front Door address if the Bastion is not specified:
```
az network bastion ssh -g <resource-group> --target-ip-address <local-vm-ip> --auth-type "password" --username azureuser
```
This requires a single Azure Front Door in the resource group.