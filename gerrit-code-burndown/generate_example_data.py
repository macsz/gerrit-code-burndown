import time

files = [
    'network/linux_net.py',
    'test.py',
    'tests/unit/api/openstack/compute/admin_only_action_common.py',
    'tests/unit/api/openstack/compute/test_admin_actions.py',
    'tests/unit/api/openstack/compute/test_block_device_mapping.py',
    'tests/unit/api/openstack/compute/test_lock_server.py',
    'tests/unit/api/openstack/compute/test_migrate_server.py',
    'tests/unit/api/openstack/compute/test_migrations.py',
    'tests/unit/api/openstack/compute/test_pause_server.py',
    'tests/unit/api/openstack/compute/test_quotas.py',
    'tests/unit/api/openstack/compute/test_suspend_server.py',
    'tests/unit/api/openstack/compute/test_virtual_interfaces.py',
    'tests/unit/api/openstack/compute/test_volumes.py',
    'tests/unit/cells/fakes.py',
    'tests/unit/cells/test_cells_manager.py',
    'tests/unit/cells/test_cells_messaging.py',
    'tests/unit/cells/test_cells_rpc_driver.py',
    'tests/unit/compute/test_compute_api.py',
    'tests/unit/conductor/tasks/test_live_migrate.py',
    'tests/unit/conductor/test_conductor.py',
    'tests/unit/consoleauth/test_consoleauth.py',
    'tests/unit/network/test_linux_net.py',
    'tests/unit/network/test_manager.py',
    'tests/unit/network/test_neutronv2.py',
    'tests/unit/objects/test_instance.py',
    'tests/unit/test_service.py',
    'tests/unit/virt/libvirt/test_driver.py',
    'tests/unit/virt/test_block_device.py',
    'tests/unit/virt/test_virt_drivers.py',
    'tests/unit/virt/vmwareapi/test_driver_api.py',
    'tests/unit/virt/xenapi/image/test_utils.py',
    'tests/unit/virt/xenapi/image/test_vdi_through_dev.py',
    'tests/unit/virt/xenapi/test_vm_utils.py',
    'tests/unit/virt/xenapi/test_vmops.py',
    'tests/unit/virt/xenapi/test_xenapi.py',
]

with open('data/num_all_files.csv', 'w') as f:
    ts = int(time.time())
    hr = 60*60
    records = 100
    c = ''
    for i in range(0, records):
        cts = ts-((records-i)*hr)
        val = len(files)-int((i/(float(records))*len(files)))
        c += '{0},{1}'.format(cts, val) + '\n'
    f.write(c)
