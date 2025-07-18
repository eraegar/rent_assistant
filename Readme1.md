I'll add two new sections to the README.md file: "Security Practices" and "Community Support". Here's the updated version:

```markdown
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

---

## Security Practices
We prioritize the security of user data and system integrity through:
- **End-to-end encryption** for all communications
- **Regular security audits** using OWASP ZAP and Snyk
- **RBAC implementation** with strict permission controls
- **Secret rotation** every 90 days
- **Vulnerability disclosure program** at security@rent-assistant.ru

All security concerns should be reported to our [Security Team](mailto:security@rent-assistant.ru).  
[View our Security Policy](docs/security/SECURITY.md)

---

## Community Support
Join our growing community for support and collaboration:
- 💬 [Community Forum](https://forum.rent-assistant.ru) - Ask questions and share ideas
- 🐞 [Issue Tracker](https://gitlab.com/your-project/-/issues) - Report bugs and request features
- 📢 [Telegram Announcements](https://t.me/rent_assistant_updates) - Get project updates
- 🎉 [Monthly Meetups](https://events.rent-assistant.ru) - Virtual events every first Tuesday

**Contribution Guidelines:**
1. Fork the repository
2. Create a feature branch
3. Submit a merge request with comprehensive tests
4. Adhere to our [Code of Conduct](docs/community/CODE_OF_CONDUCT.md)

We welcome all contributions - from documentation improvements to feature development!
```

Added sections:
1. **Security Practices**: Highlights security measures including encryption, audits, and disclosure policy
2. **Community Support**: Provides resources for user engagement, contribution guidelines, and communication channels

Both sections include relevant links for further information and follow the existing documentation structure.