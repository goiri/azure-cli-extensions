# Azure Bastion behind Azure Front Door
For some reason (security!?), accessing Azure Bastion from external IPs is not secure.
However, putting the Azure Bastion behind Azure Front Door makes everybody happy; sure.

The problem is that the `az cli` expects to connect directly to the Azure Bastion.
This hacky extension overwrites the Azure Bastion address with the Azure Front Door address.
It also ignores the mismatch of host names in the SSL handshake.

Note that this requires an Azure Front Door setup pointing to the Azure Bastion IP.

## Install the extension
We clone the remote repository, compile the extension, remove the previous version, and install the new one:
```bash
git clone https://github.com/goiri/azure-cli-extensions.git
cd azure-cli-extensions\src\bastion
pip install --upgrade setuptools wheel
python setup.py bdist_wheel
az extension remove -n bastion
az extension add --source .\dist\bastion-1.4.0-py3-none-any.whl
```

## Create Azure Front Door
One needs to create an Azure Front Door that points to the "public" DNS/IP of the Azure Bastion.

TODO provide Azure Bicep script.


## Use the extension
Now, one can pass the Azure Front Door address with the `--frontdoor` argument:
```bash
az network bastion ssh --name <bastion-name> -g <resource-group> --target-ip-address <local-vm-ip> --auth-type "password" --username azureuser --frontdoor <frontdoor-address>
```