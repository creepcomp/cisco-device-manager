# Cisco Manager

Cisco Manager is a Python-based application built with Tkinter that allows users to manage multiple Cisco devices via SSH. This tool provides a user-friendly interface for executing commands, organizing devices into groups, and backing up configurations to a TFTP server.

## Features

- **Multi-Node Management**: Connect and manage multiple Cisco devices simultaneously.
- **Group Organization**: Organize devices into groups for easier management.
- **SSH Connectivity**: Securely connect to devices using SSH.
- **Command Execution**: Execute commands on selected devices or groups.
- **Configuration Backup**: Backup device configurations to a TFTP server.
- **User -Friendly Interface**: Built with Tkinter for an intuitive user experience.

## Screenshots

![Screenshot-2025-01-08-024705.png](https://i.ibb.co/8jNRjDZ/Screenshot-2025-01-08-024705.png)

## Requirements

- Python 3.x
- Tkinter (usually included with Python installations)
- Paramiko (for SSH connectivity)
- TFTP server (for backup functionality)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/creepcomp/cisco-device-manager.git
   cd cisco-device-manager
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python main.py
   ```

## Usage

1. **Add Devices**: Use the interface to add Cisco devices by entering their IP addresses, usernames, and passwords.
2. **Create Groups**: Organize devices into groups for easier management.
3. **Execute Commands**: Select a device or group and enter the command you wish to execute.
4. **Backup Configurations**: Specify the TFTP server address and initiate the backup process for selected devices.

## Configuration

Before using the application, ensure that your TFTP server is running and accessible from the machine where you are running Cisco Manager. You may need to adjust firewall settings to allow TFTP traffic.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the developers of Paramiko for providing a robust SSH library.
- Special thanks to the open-source community for their contributions and support.

## Contact

For any questions or feedback, please reach out to creepcomp@gmail.com
