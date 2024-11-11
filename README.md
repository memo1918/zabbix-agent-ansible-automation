# Zabbix Agent2 Ansible Automation

Currently set for Zabbix 6.4, this can be changed by updating urls in the ansible playbook.
Ansible playbooks can be run for Debian and Red Hat based systems.

### Prerequisites

- Ansible installed on your control machine.
- Python and necessary dependencies listed in `ServerScript/requirements.txt`.

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/memo1918/zabbix-agent-ansible-automation.git
    cd zabbix-agent-ansible-automation
    ```

2. Install Python dependencies:
    ```sh
    pip install -r ServerScript/requirements.txt
    ```

### Usage

1. Update the inventory file with your hosts and update sv_ip with the Zabbix server ips in host_conf_zabbix.yaml.

2. Run the Ansible playbooks as needed:
    ```sh
    ansible-playbook install_zabbix_allSys.yaml -K
    ansible-playbook host_conf_zabbix.yaml -K
    ansible-playbook conf_docker_permission.yaml -K 
    ```

3. Update configIps.txt with server ip and host names and ips.

4. Update the python script to add Zabbix AUTH token or user and password.

5. Execute the Python script to manage Zabbix hosts:
    ```sh
    python ServerScript/zabbixPythonReq.py
    ```



## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Zabbix](https://www.zabbix.com/)
- [Ansible](https://www.ansible.com/)

---
