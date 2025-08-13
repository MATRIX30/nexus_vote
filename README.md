# NEXUS_VOTE

# Table of Contents

- [Description](#description)
- [Features](#features)
  - [Nexus_vote Actors and Use cases](#nexus_vote-actors-and-use-cases)
    - [Nexus_Vote Client](#nexus_vote-client)
    - [Nexus_Vote Admin](#nexus_vote-admin)
- [System Architecture](#system-architecture)
- [DevOps Workflow](#devops-workflow)
  - [CI/CD Pipeline](#1-cicd-pipeline)
    - [Continuous Monitoring with Prometheus and Grafana](#continuous-monitoring-with-prometheus-and-grafana)
  - [Orchestration with Kubernetes](#2-orchestration-with-kubernetes)
  - [Nexus Vote Data Model](#nexus-vote-data-model)
- [Installation and Setup](#installation-and-setup)
  - [Clone the Repository](#clone-the-repository)
  - [Install PostgreSQL](#install-postgresql)
    - [Windows](#windows)
    - [Linux (Ubuntu/Debian)](#linux-ubuntudebian)
    - [Linux (CentOS/RHEL/Fedora)](#linux-centosrhelfedora)
    - [macOS](#macos)
    - [Post-Installation Setup](#post-installation-setup)
  - [Install Python3](#install-python3-on-your-system)
    - [Windows](#windows-1)
    - [Linux](#linux)
    - [macOS](#macos-1)
  - [Install Python Libraries](#2-install-python-libraries)
  - [Containerization with Docker](#containerization-docker)
- [Usage](#usage)
- [Contributions Guidelines](#contributions-guidelines)
  - [How to Contribute](#how-to-contribute)
  - [Code Style Guidelines](#code-style-guidelines)
  - [Reporting Issues](#reporting-issues)
  - [Feature Requests](#feature-requests)
- [License](#license)
  - [MIT License](#mit-license)
- [Support](#support)

# Description
Nexus vote is a decentralized secure and transparent platform that enables users to rapidly create dynamic and transparent polls to get the democratic pulse of their Electorates on an opinion. This application uses a MFA mechanism to authenticate its users and a transparent dashboard to view in real time the computation of the results of a Poll. It also provides a custom authentication algorithm to prevent fraud in voting such as double voting the system uses unique generated Keys for each voter which once used can’t be used again, vote tempering the integrity of polls is guaranteed by hashing and signature to capture snapshots of states of a poll and preserve its integrity. 

# Features
1. Poll Management
    - APIs to create polls with multiple options.
	- Include metadata such as creation date and expiry.
2. Voting System
	- APIs for users to cast votes.
    - Implement validations to prevent duplicate voting.
3. Result Computation
    - Real-time calculation of vote counts for each option.
    - Efficient query design for scalability.
4. API Documentation
    - Use Swagger to document all endpoints.
    - Host documentation at /api/docs for easy access.
##	Nexus_vote Actors and Use cases
The platform has two (2) principal actors with the following use cases

#### - Nexus_Vote Client:
---
This is a normal user who can perform the following functionalities.
- Signup into the platform
- Login into the platform
- Create a poll
- Register for a poll
- Vote for a poll they are registerdd in
- View polls they are registered for.
- Search ongoing polls


#### - Nexus_Vote Admin:
---
- Signup into the platform
- Login and logout of platform
- Manage all Polls
- Manage all clients


# System Architecture
The Architecture proposed is a client server architecture with an API Component 
as the core that serves the clients
![Nexus Vote System Architecture](./imgs/Nexus_vote%20Architecture.png)
# DevOps Workflow
## 1) CI/CD Pipleline

#### - Continuous Monitory with Prometheus and Grafana
Continuous monitoring of VPS server where Nexus_vote runs using prometheus and 
Grafana

![Nexus Vote Server Monitoring](./imgs/Nexus_vote_Grafana%20Dashboard.png)
## 2) Orchestration with Kubernetes



## Nexus Vote Data Model

![Nexus Vote Data Model](./imgs/Nexus_vote%20DataModel.png)

# Installation and Setup
steps:
### Git clone DineHub Repository
---
### Clone the DineHub Repository
To get started, you need to clone the DineHub repository. Follow these steps:

1. Open your terminal or command prompt.
2. Change your current directory to the desired location where you want to clone the repository.
3. Run the following command to clone the repository:
    ```
    git clone git@github.com:MATRIX30/nexus_vote.git
    ```

Once the repository is cloned, you can proceed with the installation and setup of both the front-end and back-end components.

## Install PostgreSQL
---

Nexus Vote uses PostgreSQL as its database. Follow the instructions below to install PostgreSQL on your operating system:

### Windows:
1. Visit the [PostgreSQL official download page](https://www.postgresql.org/download/windows/)
2. Download the PostgreSQL installer for Windows
3. Run the installer and follow these steps:
   - Choose installation directory (default is recommended)
   - Select components to install (keep all defaults selected)
   - Choose data directory (default is recommended)
   - Set a password for the postgres user (remember this password!)
   - Set port number (default 5432 is recommended)
   - Choose default locale
4. Complete the installation and launch Stack Builder if prompted
5. Verify installation by opening Command Prompt and running:
   ```cmd
   psql --version
   ```

### Linux (Ubuntu/Debian):
1. Update your package list:
   ```bash
   sudo apt update
   ```
2. Install PostgreSQL:
   ```bash
   sudo apt install postgresql postgresql-contrib
   ```
3. Start and enable PostgreSQL service:
   ```bash
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   ```
4. Switch to postgres user and create a database:
   ```bash
   sudo -u postgres psql
   ```
5. Set password for postgres user (in psql prompt):
   ```sql
   \password postgres
   ```
6. Exit psql:
   ```sql
   \q
   ```

### Linux (CentOS/RHEL/Fedora):
1. Install PostgreSQL:
   ```bash
   # For CentOS/RHEL
   sudo yum install postgresql postgresql-server postgresql-contrib
   
   # For Fedora
   sudo dnf install postgresql postgresql-server postgresql-contrib
   ```
2. Initialize the database:
   ```bash
   sudo postgresql-setup initdb
   ```
3. Start and enable PostgreSQL:
   ```bash
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   ```

### macOS:
1. **Using Homebrew (Recommended):**
   ```bash
   # Install Homebrew if not already installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install PostgreSQL
   brew install postgresql
   
   # Start PostgreSQL service
   brew services start postgresql
   ```

2. **Using PostgreSQL App:**
   - Download Postgres.app from [postgresapp.com](https://postgresapp.com/)
   - Drag to Applications folder and launch
   - Click "Initialize" to create a new server

3. **Using Official Installer:**
   - Download from [PostgreSQL official site](https://www.postgresql.org/download/macosx/)
   - Follow the installation wizard

### Post-Installation Setup:
1. **Create a database for Nexus Vote:**
   ```bash
   # Connect to PostgreSQL
   psql -U postgres
   
   # Create database
   CREATE DATABASE nexus_vote_db;
   
   # Create a user for the application
   CREATE USER nexus_user WITH PASSWORD 'your_password';
   
   # Grant privileges
   GRANT ALL PRIVILEGES ON DATABASE nexus_vote_db TO nexus_user;
   
   # Exit
   \q
   ```

2. **Verify Installation:**
   ```bash
   psql --version
   ```

### Configuration Notes:
- Default PostgreSQL port: 5432
- Default superuser: postgres
- Remember to update your Django settings.py with the correct database credentials
- For production, consider additional security configurations

## Install python3 on your system
---

The backend is build with python. so you need to install python3 to do that:
### 1) install python3 on your system
The backend is built with Python, so you need to install Python3 to proceed. Follow the instructions below based on your operating system:

##### - Windows:
1. Head over to the [Python official website](https://www.python.org/downloads/windows/) and download the latest version of Python for Windows.
2. Run the installer and select the option to add Python to your system's PATH.
3. Follow the prompts to complete the installation.

##### - Linux:
1. Open a terminal.
2. Run the following command to install Python3:
    ```
    sudo apt-get update
    sudo apt-get install python3
    ```

##### - macOS:
1. Open a terminal.
2. Install Homebrew by running the following command:
    ```
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
3. Once Homebrew is installed, run the following command to install Python3:
    ```
    brew install python3
    ```

After installing Python, you can proceed with next step.


### 2) Install Python Libraries
To install the required Python libraries for the backend, follow these steps:

1. Open your terminal or command prompt.
2. Change your current directory to the backend folder by running the following command:
    ```
    cd /home/nexus_vote/backend
    ```
3. Once you are inside the backend folder, run the following command to install the required libraries from the `requirements.txt` file:
    ```
    pip3 install -r requirements.txt
    ```

This will install all the necessary Python libraries for the Nexus_vote backend.

##### - Contiainerization Docker:
To pull and run Nexus_vote container image run the following command 
```
docker run 
```


# Usage
To run the API Back-end run the following command
```
python3 manage.py runserver 
```
# Contributions Guidelines

We welcome contributions to Nexus Vote! Please follow these guidelines to ensure a smooth contribution process:

## How to Contribute

### 1. Fork the Repository
- Fork the repository on GitHub
- Clone your fork locally:
  ```bash
  git clone https://github.com/YOUR_USERNAME/nexus_vote.git
  cd nexus_vote
  ```

### 2. Create a Feature Branch
- Create a new branch for your feature or bug fix:
  ```bash
  git checkout -b feature/your-feature-name
  ```

### 3. Make Your Changes
- Follow the existing code style and conventions
- Write clear, concise commit messages
- Add tests for new functionality
- Update documentation as needed

### 4. Test Your Changes
- Run the existing tests to ensure nothing is broken
- Add new tests for your changes
- Ensure all tests pass before submitting

### 5. Submit a Pull Request
- Push your changes to your fork
- Create a pull request with a clear description of your changes
- Reference any related issues

## Code Style Guidelines
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused

## Reporting Issues
- Use the GitHub issue tracker to report bugs
- Provide detailed information about the issue
- Include steps to reproduce the problem
- Add relevant screenshots if applicable

## Feature Requests
- Use the GitHub issue tracker for feature requests
- Clearly describe the proposed feature
- Explain the use case and benefits

# License 

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## MIT License

```
MIT License

Copyright (c) 2025 MATRIX30

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

# Support

If you need help or have questions about Nexus Vote, please reach out:

- **Email**: matrixboy30@gmail.com
- **GitHub Issues**: [Create an issue](https://github.com/MATRIX30/nexus_vote/issues)
- **Documentation**: Check the docs/ folder for detailed documentation

For urgent issues or security concerns, please email directly at matrixboy30@gmail.com

