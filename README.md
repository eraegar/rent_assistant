**Assistant For Rent**  
![Project logo](App/afrlogo.jpg)  

**Service for renting personal or business assistants to complete tasks**  

🌐 [Live Application](https://rent-assistant.ru)  

---  

## Project Goals and Description  
A system for renting personal/business assistants to complete tasks:  
- Three-role structure (managers/assistants/clients)  
- Telegram integration for notifications and interaction  
- Task management  
- Automated workflows  

---  

## Context Diagram  
```mermaid  
graph LR  
    A[Manager] --> B[Frontend]  
    C[Assistant] --> B  
    D[Client] --> B  
    B --> E[Backend API]  
    E --> F[(Database)]  
    E --> G[Telegram Bot]  
    G --> H[Telegram Cloud]  
    H --> C  
    H --> D  
```  

---  

## Roadmap  
### Completed  
- [x] Object management  
- [x] Task assignment to assistants  
- [x] Telegram notifications  
- [x] Multi-role interfaces  
- [x] User filtering system  

### In Development  
- [ ] Payment integration  
- [ ] AI assistant  
- [ ] Communication chat  

---  

## User Guide  
### For Managers  
1. Log in at [manager.rent-assistant.ru](https://manager.rent-assistant.ru)  
2. Assign tasks to assistants  
3. Track task completion  

### For Assistants  
1. Use [assistant.rent-assistant.ru](https://assistant.rent-assistant.ru)  
2. View assigned tasks  
3. Mark tasks as completed  
4. **Important:** Always check task deadlines  

### For Clients  
1. Create a task at [rent-assistant.ru](https://rent-assistant.ru)  
2. Submit a completion request  
3. Receive updates via Telegram  

[Full Guide](docs/usage-guide.md)  

---  

## Installation and Deployment  
```bash  
# 1. Clone repository  
git clone https://gitlab.com/your-project/rent-assistant.git  
cd rent-assistant  

# 2. Install dependencies  
npm install  
pip install -r requirements.txt  

# 3. Configure environment  
cp .env.example .env  

# Update values in .env file:  
#   BOT_TOKEN=your_telegram_token  
#   DB_URL=postgresql://user:password@localhost/dbname  

# 4. Launch system  
docker-compose up --build  
```  

Environment requirements:  
- Docker 20.10+  
- Node.js 18.x  
- Python 3.10+  

[Detailed Instructions](docs/deployment.md)  

---  

## Documentation  
### Development  
- [Kanban Board](https://gitlab.com/your-project/-/boards)  
- [Git Workflow](docs/git-workflow.md)  
- [Secrets Management](docs/secrets-management.md)  
- [CONTRIBUTING.md](CONTRIBUTING.md)  

### Quality Assurance  
- [Quality Attributes](docs/quality-attributes/quality-attribute-scenarios.md)  
- [Automated Tests](docs/quality-assurance/automated-tests.md)  
- [User Acceptance Tests](docs/quality-assurance/user-acceptance-tests.md)  

### Automation  
- [Continuous Integration](docs/automation/continuous-integration.md)  
- [Continuous Delivery](docs/automation/continuous-delivery.md)  

### Architecture  
- [System Architecture](docs/architecture/architecture.md)  
- [Static View](docs/architecture/static-view.md)  
- [Dynamic View](docs/architecture/dynamic-view.md)  
- [Deployment View](docs/architecture/deployment-view.md)  

---  

## Changelog  
All notable changes in [CHANGELOG.md](CHANGELOG.md):  
```markdown  
# Changelog  

## [2.5.0]  
### Added  
- Advanced user filtering  
- Request caching system  
- Performance optimization  

## [2.0.0]  
### Added  
- Telegram integration  
- Multi-role interface  
- Task management system  

## [1.0.0]  
### Added  
- Basic property management functionality  
- Authentication system  
- API for core operations  
```  

---  

## Tech Stack  
**Frontend:**  
- React 18  
- Redux Toolkit  
- Material UI  

**Backend:**  
- Python 3.10  
- FastAPI  
- SQLAlchemy  

**Infrastructure:**  
- Docker  
- GitLab CI/CD  
- Ubuntu Server  
- Cloudflare Tunnel
### Assistant For Rent
![Project logo](App/afrlogo.jpg)

**A service for renting a personal or business assistant to complete tasks**

🌐 [Live Application](https://rent-assistant.ru)

---

## Project Goals and Description
A system for renting a personal/business assistant to complete tasks:
- Three-role structure (managers/assistants/clients)
- Telegram integration for notifications and interaction
- Task management
- Automated workflows

---

## Context Diagram
```mermaid
graph LR
    A[Manager] --> B[Frontend]
    C[Assistant] --> B
    D[Client] --> B
    B --> E[Backend API]
    E --> F[(Database)]
    E --> G[Telegram Bot]
    G --> H[Telegram Cloud]
    H --> C
    H --> D
```

---

## Roadmap
### Implemented
- [x] Object management
- [x] Task assignment to assistants
- [x] Telegram notifications
- [x] Multi-role interfaces
- [x] User filtering system

### In Development
- [ ] Payment integration
- [ ] AI assistant
- [ ] Chat for communication

---

## User Guide
### For Managers
1. Log in at [manager.rent-assistant.ru](https://manager.rent-assistant.ru)
2. Assign tasks to assistants
3. Track task completion

### For Assistants
1. Use [assistant.rent-assistant.ru](https://assistant.rent-assistant.ru)
2. View assigned tasks
3. Mark tasks as completed
4. Important: always check task deadlines

### For Clients
1. Create a task at [rent-assistant.ru](https://rent-assistant.ru)
2. Submit a request for execution
3. Receive updates via Telegram

[Full Guide](docs/usage-guide.md)

---

## Installation and Deployment
```bash
# 1. Clone the repository
git clone https://gitlab.com/your-project/rent-assistant.git
cd rent-assistant

# 2. Install dependencies
npm install
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env

# Update values in the .env file:
#   BOT_TOKEN=your_telegram_token
#   DB_URL=postgresql://user:password@localhost/dbname

# 4. Start the system
docker-compose up --build
```

Environment requirements:
- Docker 20.10+
- Node.js 18.x
- Python 3.10+

[Detailed instructions](docs/deployment.md)

---

## Documentation
### Development
- [Kanban board](https://gitlab.com/your-project/-/boards)
- [Git workflow](docs/git-workflow.md)
- [Secrets management](docs/secrets-management.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)

### Quality Assurance
- [Quality attributes](docs/quality-attributes/quality-attribute-scenarios.md)
- [Automated tests](docs/quality-assurance/automated-tests.md)
- [User acceptance tests](docs/quality-assurance/user-acceptance-tests.md)

### Automation
- [Continuous integration](docs/automation/continuous-integration.md)
- [Continuous delivery](docs/automation/continuous-delivery.md)

### Architecture
- [System architecture](docs/architecture/architecture.md)
- [Static view](docs/architecture/static-view.md)
- [Dynamic view](docs/architecture/dynamic-view.md)
- [Deployment view](docs/architecture/deployment-view.md)

---

## Changelog
All significant changes in [CHANGELOG.md](CHANGELOG.md):
```markdown
# Changelog

## [2.5.0]
### Added
- Extended user filtering
- Request caching system
- Performance optimization

## [2.0.0]
### Added
- Telegram integration
- Multi-role interface
- Task management system

## [1.0.0]
### Added
- Basic real estate management functionality
- Authentication system
- API for core operations
```

---

## Telegram Commands
To access role-specific interfaces via the Telegram bot, send one of the following commands:

менеджер — to access the manager interface

ассистент — to access the assistant interface

The bot will guide the user to the appropriate interface based on the command.

## Deployment on Customer's Server
To deploy the project on a customer's server:

# 1. Clone the repository
git clone https://gitlab.com/your-project/rent-assistant.git
cd rent-assistant

# 2. Set environment variables
cp .env.example .env
# Update .env with production values

# 3. Launch services
docker-compose up -d --build
Ensure the server has Docker and Docker Compose installed.
For custom domain and HTTPS, configure Cloudflare Tunnel or use your own reverse proxy.

## Tech Stack
**Frontend:**
- React 18
- Redux Toolkit
- Material UI

**Backend:**
- Python 3.10
- FastAPI
- SQLAlchemy

**Infrastructure:**
- Docker
- GitLab CI/CD
- Ubuntu Server
- Cloudflare Tunnel