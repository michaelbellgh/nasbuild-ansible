import yaml, getpass

vm_vars_file = "data/nas/vars/vm.yml"
vars = yaml.load(open(vm_vars_file))

def get_boolean(prompt):
    output = input(prompt + ": ")
    while output.lower() not in ("true", "false", "yes", "no"):
        print("Please enter one of the following: True, False, Yes, No")
        output = input(prompt)
    if output.lower() in ("true, yes"):
        return True
    elif output.lower() in ("false, no"):
        return False
    else:
        return False

def get_string(prompt):
    output = input(prompt + ": ")
    while output == "":
        print("Please enter a value")
        output = input(prompt + ": ")
    return output

def get_integer(prompt, min, max):
    output = input(prompt + ": ")
    while not output.isdigit() and (output > max and output < min):
        print("Please enter a value between " + str(min) + " and " + str(max))
        output = input(prompt + ": ")
    return output


vars['options']['delete_existing'] = get_boolean("Rebuild VM?")
vars['options']['validate_certs'] = get_boolean("Validate ESXi certs?")
vars['options']['copy_iso'] = get_boolean("Copy ISO?")

vars['paths']['src_iso'] = get_string("Source ISO?")
vars['paths']['target_datastore'] = get_string("Datastore name?")
vars['paths']['target_folder'] = get_string("Datastore folder?")
vars['paths']['target_iso_filepath'] = get_string("Destination filepath for ISO?")

vars['vminfo']['vm_id'] = get_string("VM Name?")
vars['vminfo']['guest_id'] = get_string("VM Guest type? [ubuntu64guest]")
vars['vminfo']['hostname'] = get_string("Hostname?")
vars['vminfo']['domain'] = get_string("Domain?")
vars['vminfo']['dns_suffix'] = get_string("DNS Suffix?")
vars['vminfo']['disk_size_gb'] = get_integer("Main disk size in GB?", 10, 2048)
vars['vminfo']['memory_mb'] = get_integer("Memory in MB?", 256, 65536)
vars['vminfo']['num_cpus'] = get_integer("CPU count?", 1, 32)
vars['vminfo']['cores_per_cpu'] = get_integer("Cores per cpu counts", 1, 32)
vars['vminfo']['service_user'] = get_string("Service user account?")

staging_networks_input = get_string("Initial staging networks? Comma separated list of VMWare port groups")
staging_networks_list = [x.strip() for x in staging_networks_input.split(",")]
results = []
for x in staging_networks_list:
    results.append({"name" : x})
vars['vminfo']['staging_networks'] = results

final_network_input = get_string("Final networks? Comma separated list of VMWare port groups")
final_networks_list = [x.strip() for x in final_network_input.split(",")]
results = []
for x in final_networks_list:
    results.append({"name" : x})
vars['vminfo']['networks'] = results


vars['creds']['guest_user'] = get_string("Guest OS username? Note: Must be already created during installation")
vars['creds']['guest_pass'] = getpass.getpass("Guest password for " + vars['creds']['guest_user'] + "?: ")

print(vars)


yaml.dump(vars, open(vm_vars_file, 'w'))