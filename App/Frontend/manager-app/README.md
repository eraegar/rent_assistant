# Manager Dashboard - Telegram Assistant

This is a separate React application for the management dashboard of the Telegram Assistant service.

## Architecture

- **Port**: 3001 (different from main client app on port 3000)
- **Authentication**: Uses manager-specific JWT tokens
- **API**: Connects to the same backend API at `localhost:8000`
- **Storage**: Separate localStorage keys (`manager_token` vs `auth_token`)

## Setup & Installation

1. **Install dependencies**:
   ```bash
   cd manager-app
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm start
   ```
   
   The app will run on http://localhost:3001

## Manager Registration

Before using the dashboard, you need to register a manager account:

```bash
# From the project root, run the backend
cd app
python main.py

# Then register a manager (use test_manager_api.py as reference)
curl -X POST http://localhost:8000/api/v1/management/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Admin Manager",
    "phone": "+1234567890", 
    "password": "admin123",
    "email": "admin@company.com",
    "department": "Operations"
  }'
```

## Usage

1. **Login**: Use your manager phone number and password
2. **Dashboard**: View overview analytics, tasks, assistants, and clients
3. **Logout**: Click the logout button in the top-right corner

## Differences from Client App

| Feature | Client App (port 3000) | Manager App (port 3001) |
|---------|----------------------|------------------------|
| Users | Customers | Managers |
| Authentication | `/api/v1/auth/*` | `/api/v1/management/auth/*` |
| Token Key | `auth_token` | `manager_token` |
| Features | Task creation, payments | Analytics, user management |
| Theme | Purple (`#6c7ee1`) | Blue (`#1976d2`) |

## Development

- **TypeScript**: Fully typed with strict mode
- **Material-UI**: Same component library as main app
- **Zustand**: State management for authentication
- **React Router**: Simple routing (login/dashboard)

## Production Deployment

For production, build and serve on a different subdomain:

```bash
npm run build
# Serve build/ on manager.yourapp.com
```

## API Endpoints Used

- `POST /api/v1/management/auth/login`
- `GET /api/v1/management/profile` 
- `GET /api/v1/management/dashboard/overview`
- `GET /api/v1/management/tasks`
- `GET /api/v1/management/assistants`
- `GET /api/v1/management/clients` 