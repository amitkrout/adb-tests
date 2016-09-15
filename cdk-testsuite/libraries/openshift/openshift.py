'''
Created on Jun 29, 2016

@author: amit
'''
from avocado.utils import process
import imp
import logging
import time

log = logging.getLogger("Openshift.Debug")

def openshiftLibInfo(self):
    '''
    Get openshift user defined library version
    Args:
        self (object): Object of the current method
    '''
    openshiftUtils = imp.load_source('openshiftUtils', self.params.get('openshift_util_MODULE'))
    self.log.info("Openshift library version : " +openshiftUtils.get_version())
    
def oc_usr_login(self, ip_port, uname, password):
    '''
    Login to openshift server and returns output of the oc command executed
    Args:
        self (object): Object of the current method
        ip_port (str): ip and port of openshift to be used
        uname (str): username of openshift web console to be used
        password (str): password of openshift web console to be used
    '''
    output = "FAIL"
    strcmd = "vagrant ssh -c 'oc login " +ip_port +" --username=" +uname +" --password=" +password +" --insecure-skip-tls-verify" +"'"
    self.log.info ("Executing : " +strcmd)
    try:
        output = process.system_output(strcmd)
    except:
        return output
    return output

def add_new_project(self, project_name):
    '''
    Adding new project to openshift server and returns output of the oc command executed
    Args:
        self (object): Object of the current method
        project_name (str): name of the project to be added to the openshift server
    '''
    output = "FAIL"
    strcmd = "vagrant ssh -c 'oc new-project " +project_name +"'"
    self.log.info ("Executing : " +strcmd)
    time.sleep(2)
    try:
        output = process.system_output(strcmd)
    except:
        return output
    return output

def add_new_app(self, registry):
    '''
    Adding new application to new project created for openshift server and returns output of the oc command executed
    Args:
        self (object): Object of the current method
        registry (str): registry path/location
    '''
    output = "FAIL"
    strcmd = "vagrant ssh -c 'oc new-app " +registry +"'"
    lst = registry.split("/")
    repo = lst[len(lst) - 1]
    self.log.info ("Executing : " +strcmd)
    time.sleep(2)
                
    lst = []
    try:
        output = process.system_output(strcmd)
    except:
        return output
    for lines in output.splitlines():
        if repo in lines:
            lst.append(lines)
                
    lst = lst[len(lst) - 1].split("'") 
    strcmd1 = "vagrant ssh -c " +"'" +lst[1] +"'"
    self.log.info ("Executing : " +strcmd1) 
    time.sleep(60)
                       
    try:
        output = process.system_output(strcmd1)
    except:
        return output
    strcmd2 = "vagrant ssh -c 'oc status -v'"
    self.log.info ("Executing : " +strcmd2)
    time.sleep(2)
    try:
        output = process.system_output(strcmd2)
    except:
        return output
    return output

def oc_port_expose(self, service_name):
    '''
    Service port to expose outside and returns output of the oc command executed
    Args:
        self (object): Object of the current method
        service_name (str): name of the service to be exposed outside
    '''
    strcmd = "vagrant ssh -c 'oc expose service " +service_name +"'"
    time.sleep(60)
    output = "FAIL"
    try:
        output = process.system_output(strcmd)
    except:
        return output
    return output

def oc_get_service(self):
    '''
    Get the service name of the application and returns output of the oc command executed
    Args:
        self (object): Object of the current method
    '''
    strcmd = "vagrant ssh -c 'oc get service'"
    output = "FAIL"
    try:
        output = process.system_output(strcmd)
    except:
        return output
    return output

def oc_get_pod(self):
    '''
    Get the pods details of the containerized application and returns output of the oc command executed
    Args:
        self (object): Object of the current method
    '''
    strcmd = "vagrant ssh -c 'oc get pod'"
    output = "FAIL"
    try:
        output = process.system_output(strcmd)
    except:
        return output
    return output

def routing_cdk(self, service_name, openshift_project_name):
    '''
    Runs landrush server returns output of the oc command executed
    Args:
        self (object): Object of the current method
        service_name (string): name of the service to be exposed outside
        openshift_project_name (string): name of the project to be added to the openshift server
    '''
    time.sleep(60)
    output = "FAIL"
    strcmd = "vagrant ssh -c 'oc get route'"
    try:
        output = process.system_output(strcmd)
        for lines in output.split():
            if service_name +"-" +openshift_project_name in lines:
                strcmd = "curl -I http://" +lines
                output = process.system_output(strcmd)
    except:
        return output
    return output

def oc_delete(self, project_name):
    '''
    Delete the openshift project and returns output of the oc command executed
    Args:
        self (object): Object of the current method
        openshift_project_name (string): name of the project to be added to the openshift server
    '''
    strcmd = "vagrant ssh -c 'oc delete project " +project_name +"'"
    time.sleep(15)
    output = "FAIL"
    try:
        output = process.system_output(strcmd)
    except:
        return output
    return output

def oc_logout(self):
    '''
    logout from openshift server and returns output of the oc command executed
    Args:
        self (object): Object of the current method
    '''
    strcmd = "vagrant ssh -c 'oc logout'"
    self.log.info ("Executing : " +strcmd)
    output = "FAIL"
    try:
        output = process.system_output(strcmd)
    except:
        return output
    return output

def add_new_template(self, template):
    '''
    Adding new template to openshift server and returns output of the oc command executed
    Args:
        self (object): Object of the current method
        template (string): name of the openshift template
    '''
    strcmd = "vagrant ssh -c 'oc new-app --template=" +template +"'"
    self.log.info ("Executing : " +strcmd)
        
    lst = []
    output = "FAIL"
    try:
        output = process.system_output(strcmd)
    except:
        return output
    for lines in output.splitlines():
        if template in lines:
            lst.append(lines)
                
    lst = lst[len(lst) - 1].split("'") 
    strcmd1 = "vagrant ssh -c " +"'" +lst[1] +"'"
    self.log.info ("Executing : " +strcmd1) 
    time.sleep(30)
    try:
        output = process.system_output(strcmd1)
    except:
        return output
    
    strcmd2 = "vagrant ssh -c 'oc status -v'"
    self.log.info ("Executing : " +strcmd2)
    time.sleep(2)
    try:
        output = process.system_output(strcmd2)
    except:
        return output
    return output
