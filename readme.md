# AzDo2Tf

This reposito contain an script that import existing Azure DevOps objects to Terraform code [Terraform Azure DevOps provider](https://github.com/microsoft/terraform-provider-azuredevops/)

## Getting startd

### requirements
 - Install the Azure DevOps python cli , with the command ```pip install azure-devops```
 - Create an Azure DevOps Token (PAT) [Documentation](https://docs.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=preview-page)

### Run the python script

For generate the Terrform code for all projects inside an organization:
```python azdo2tf.py -o "<path of the generation>" --pat "<your AZDO PAT>" --organization "<Uri for your AZDO organization>"```

For generate the Terrform code for 1 specific projects inside an organization:
```python azdo2tf.py -o "<path of the generation>" --pat "<your AZDO PAT>" --organization "<Uri for your AZDO organization>" --project "<Name of the project>"```

sample:
```python /mnt/d/Repos/azdo2tf/azdo2tf.py -o "/mnt/d/.gen" --pat "a2vxpitnuc7fyl6dxxxxxxxxxxxxxxxxxxxx" --organization "https://dev.azure.com/MyOrga" --project "Test Project"```