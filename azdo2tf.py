from azure.devops.connection import Connection
from azure.devops.v5_1.task_agent import TaskAgent
from msrest.authentication import BasicAuthentication


import pprint
import os
import argparse
import json
import subprocess

import terraform
import shutil

def generate_provider():
    providertf = os.path.join(dir, "provider.tf")
    tf = open(providertf, 'w')
    tf.write('provider "azuredevops" {\n')
    tf.write('\t version = ">= 0.0.1" \n')
    tf.write('}\n')
    tf.close()

def generate_projects(filename, project_details):
    tftype = "azuredevops_project"
    tfname = project_details.name.replace(".", "-").replace(" ", "-")
    tf = open(filename, 'w+')
    tf.write('resource "' + tftype + '" "' + tfname + '" {\n')
    tf.write('\t project_name = "' + project_details.name + '"\n')
    if project_details.description is not None:
        tf.write('\t description = "' + project_details.description + '"\n')
    tf.write('\t visibility = "' + project_details.visibility + '"\n')
    tf.write(
        '\t version_control = "' + project_details.capabilities['versioncontrol']['sourceControlType'] + '"\n')
    tf.write('\t work_item_template = "' + project_details.capabilities['processTemplate']['templateName'] + '"\n')
    tf.write('}\n')
    tf.close()
    return "{}.{}".format(tftype, tfname)


def generate_import_command(tfname, id):
    cmdline = 'terraform import {} "{}" \n'.format(tfname, id)
    sh = open(os.path.join(dir, "import.sh"), 'a')
    sh.write(cmdline)
    sh.close()


def getfilename(projectname):
    rname = projectname.replace(".", "-").replace(" ", "-") + ".tf"
    tffile = os.path.join(dir, rname)
    return tffile


def remove_file(file):
    if os.path.exists(file):
        os.remove(file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", required=True, help="generated output TF")
    parser.add_argument("-t", "--pat", required=True, help="Azure DevOps Personnal Access Token")
    parser.add_argument("--organization", required=True, help="Organization Url")
    parser.add_argument("--project", required=False, help="Project")
    args = parser.parse_args()


    # Create the .generated folder
    dir = os.path.join(args.output)
    if os.path.exists(dir):
        shutil.rmtree(dir, ignore_errors=True)
    os.mkdir(dir)

    # Fill in with your personal access token and org URL
    personal_access_token = args.pat
    organization_url = args.organization

    # Create a connection to the org
    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)

    os.chdir(dir)
    print(os.getcwd())
    os.environ["AZDO_PERSONAL_ACCESS_TOKEN"] = args.pat
    os.environ["AZDO_ORG_SERVICE_URL"] = args.organization

    remove_file(os.path.join(dir, "import.sh"))
    remove_file(os.path.join(dir, "terraform.tfstate"))

    # Generate the provider.tf
    generate_provider()

    # Get a client (the "core" client provides access to projects, teams, etc)
    core_client = connection.clients_v5_1.get_core_client()
    taskagent_client = connection.clients_v5_1.get_task_agent_client()
    taskagent_client.get_variable_groups("Test project")
    

    # Get the first page of projects

    if args.project is None:
        get_projects_response = core_client.get_projects()
    else:
        get_projects_response = core_client.get_project(args.project)
        #print(get_projects_response)
    index = 0

    if get_projects_response is not None:

        if args.project is None:
            for project in get_projects_response.value:  # List All Projects
                # print(project)


                get_details_response = core_client.get_project(project.id, include_capabilities=True)

                terraformfile = getfilename(get_details_response.name)

                terraform_resource = generate_projects(terraformfile, get_details_response)

                generate_import_command(terraform_resource, get_details_response.id)


            if get_projects_response.continuation_token is not None and get_projects_response.continuation_token != "":
                # Get the next page of projects
                get_projects_response = core_client.get_projects(
                    continuation_token=get_projects_response.continuation_token)
            else:
                # All projects have been retrieved
                get_projects_response = None

        else:  # Single Project
            print(taskagent_client.get_variable_groups(get_projects_response.id))

            get_details_response = core_client.get_project(get_projects_response.id, include_capabilities=True)

            terraformfile = getfilename(get_details_response.name)

            terraform_resource = generate_projects(terraformfile, get_details_response)

            generate_import_command(terraform_resource, get_details_response.id)



    terraform.terraform_init(dir)

    terraform.run_import(os.path.join(dir, "import.sh"))

    terraform.terraform_plan(dir)
