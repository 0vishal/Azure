'''
@Author: Vishal Salaskar
@Date: 2021-06-4
@Last Modified by: Vishal Salaskar
@Last Modified time: 2021-06-4
@Title : Program to perform copy activity with data factory 
'''

from azure.identity import ClientSecretCredential 
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import *
from datetime import datetime, timedelta
import time
import os

def print_item(group):
    """Print an Azure object instance."""
    print("\tName: {}".format(group.name))
    print("\tId: {}".format(group.id))
    if hasattr(group, 'location'):
        print("\tLocation: {}".format(group.location))
    if hasattr(group, 'tags'):
        print("\tTags: {}".format(group.tags))
    if hasattr(group, 'properties'):
        print_properties(group.properties)

def print_properties(props):
    """Print a ResourceGroup properties instance."""
    if props and hasattr(props, 'provisioning_state') and props.provisioning_state:
        print("\tProperties:")
        print("\t\tProvisioning State: {}".format(props.provisioning_state))
    print("\n\n")

def print_activity_run_details(activity_run):
    """Print activity run details."""
    print("\n\tActivity run details\n")
    print("\tActivity run status: {}".format(activity_run.status))
    if activity_run.status == 'Succeeded':
        print("\tNumber of bytes read: {}".format(activity_run.output['dataRead']))
        print("\tNumber of bytes written: {}".format(activity_run.output['dataWritten']))
        print("\tCopy duration: {}".format(activity_run.output['copyDuration']))
    else:
        print("\tErrors: {}".format(activity_run.error['message']))

class DFOperations:

    def __init__(self):
         # Azure subscription ID
        self.subscription_id = os.getenv('SUBID')

        # This program creates this resource group. If it's an existing resource group, comment out the code that creates the resource group
        self.rg_name = os.getenv('RG')

        # The data factory name. It must be globally unique.
        self.df_name = os.getenv('DF')

        self.ls_name = os.getenv('LSNAME')

        # Specify your Active Directory client ID, client secret, and tenant ID
        self.credentials = ClientSecretCredential(client_id=os.getenv('CLIENTID'), client_secret=os.getenv('CLIENTSECRET'), tenant_id=os.getenv('TENANTID')) 
        self.resource_client = ResourceManagementClient(self.credentials, self.subscription_id)
        self.adf_client = DataFactoryManagementClient(self.credentials, self.subscription_id)

    def create_factory(self):
        """
		Description
 		Function To create a data factory with name and properties
		"""
        try:

            rg_params = {'location':'westus'}
            self.resource_client.resource_groups.create_or_update(self.rg_name, rg_params)

            #Create a data factory
            df_resource = Factory(location='westus')
            df = self.adf_client.factories.create_or_update(self.rg_name, self.df_name, df_resource)
            print_item(df)
            while df.provisioning_state != 'Succeeded':
                df = self.adf_client.factories.get(self.rg_name, self.df_name)
                time.sleep(1)    
        except Exception as e:
            print(e)

    def create_linkedservice(self):
        """
		Description
 		Function To create a linked service connection for storage account in data factory
		"""
        try:

            # IMPORTANT: specify the name and key of your Azure Storage account.
            storage_string = SecureString(value=os.getenv('BLOBSTORAGESTRING'))

            ls_azure_storage = LinkedServiceResource(properties=AzureStorageLinkedService(connection_string=storage_string)) 
            ls = self.adf_client.linked_services.create_or_update(self.rg_name, self.df_name, self.ls_name, ls_azure_storage)
            print_item(ls)
        except Exception as e:
            print(e)     

    def create_dataset(self):
        """
		Description
 		Function To create input and output dataset in data factory
		"""
        try:
            
            print("Enter the filename to copy to destination")
            filename = input()
            # Create an Azure blob dataset (input)
            ds_name = 'ds_in'
            ds_ls = LinkedServiceReference(reference_name=self.ls_name)
            blob_path = os.getenv('INPUTPATH')
            blob_filename = filename
            ds_azure_blob = DatasetResource(properties=AzureBlobDataset(
                linked_service_name=ds_ls, folder_path=blob_path, file_name=blob_filename)) 
            ds = self.adf_client.datasets.create_or_update(
                self.rg_name, self.df_name, ds_name, ds_azure_blob)
            print_item(ds)

            # Create an Azure blob dataset (output)
            dsOut_name = 'ds_out'
            output_blobpath = os.getenv('OUTPUTPATH')
            dsOut_azure_blob = DatasetResource(properties=AzureBlobDataset(linked_service_name=ds_ls, folder_path=output_blobpath))
            dsOut = self.adf_client.datasets.create_or_update(
                self.rg_name, self.df_name, dsOut_name, dsOut_azure_blob)
            print_item(dsOut)    

            act_name = os.getenv('ACTNAME')
            blob_source = BlobSource()
            blob_sink = BlobSink()
            dsin_ref = DatasetReference(reference_name=ds_name)
            dsOut_ref = DatasetReference(reference_name=dsOut_name)
            self.copy_activity = CopyActivity(name=act_name,inputs=[dsin_ref], outputs=[dsOut_ref], source=blob_source, sink=blob_sink)
        except Exception as e:
            print(e)

    def run_pipeline(self):
        """
		Description
 		Function To run a pipeline for the copy activity
		"""
        try:

            p_name = os.getenv('PNAME')
            params_for_pipeline = {}
            p_obj = PipelineResource(activities=[self.copy_activity], parameters=params_for_pipeline)
            p = self.adf_client.pipelines.create_or_update(self.rg_name, self.df_name, p_name, p_obj)
            print_item(p)

            # Create a pipeline run
            run_response = self.adf_client.pipelines.create_run(self.rg_name, self.df_name, p_name, parameters={})

            # Monitor the pipeline run
            time.sleep(30)
            pipeline_run = self.adf_client.pipeline_runs.get(
                self.rg_name, self.df_name, run_response.run_id)
            print("\n\tPipeline run status: {}".format(pipeline_run.status))
            filter_params = RunFilterParameters(
                last_updated_after=datetime.now() - timedelta(1), last_updated_before=datetime.now() + timedelta(1))
            query_response = self.adf_client.activity_runs.query_by_pipeline_run(
                self.rg_name, self.df_name, pipeline_run.run_id, filter_params)
            print_activity_run_details(query_response.value[0])
        except Exception as error:
            print(error)    
