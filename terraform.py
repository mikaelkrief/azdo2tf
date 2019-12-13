import subprocess
import os


def terraform_fmt(tfdir):
    os.chdir(tfdir)
    p = subprocess.Popen('terraform fmt', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, b''):
        print(line)
    p.stdout.close()
    p.wait()

def terraform_init(tfdir):
    os.chdir(tfdir)
    p = subprocess.Popen('terraform init', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, b''):
        print(line)
    p.stdout.close()
    p.wait()


def terraform_plan(tfdir):
    os.chdir(tfdir)
    p = subprocess.Popen('terraform plan', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, b''):
        print(line)
    p.stdout.close()
    p.wait()


def run_import(shellscript):
    p = subprocess.Popen(shellscript, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, b''):
        print(line)
    p.stdout.close()
    p.wait()