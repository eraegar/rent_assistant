# **API Endpoints Specification for Backend Developer**

## **Base URL Structure**
```
Production: https://api.assistant-for-rent.com
Development: http://localhost:8000
API Version: /api/v1
```

---

## **1. CLIENT API ENDPOINTS**

### **Authentication & Profile**
```http
POST   /api/v1/clients/auth/register          # Client registration
POST   /api/v1/clients/auth/login             # Client login
POST   /api/v1/clients/auth/logout            # Client logout
GET    /api/v1/clients/profile                # Get client profile
PUT    /api/v1/clients/profile                # Update client profile
POST   /api/v1/clients/auth/refresh-token     # Refresh JWT token
POST   /api/v1/clients/auth/verify-telegram   # Verify Telegram username
```

### **Subscription Management**
```http
GET    /api/v1/clients/subscription           # Get current subscription
GET    /api/v1/clients/subscription/plans     # Available subscription plans
POST   /api/v1/clients/subscription/upgrade   # Upgrade subscription
POST   /api/v1/clients/subscription/cancel    # Cancel subscription
GET    /api/v1/clients/subscription/history   # Subscription history
```

### **Task Management**
```http
POST   /api/v1/clients/tasks                  # Create new task
GET    /api/v1/clients/tasks                  # Get all client's tasks
GET    /api/v1/clients/tasks/{task_id}        # Get specific task details
PUT    /api/v1/clients/tasks/{task_id}        # Update task (if not claimed)
DELETE /api/v1/clients/tasks/{task_id}        # Cancel task (if not claimed)
```

### **Task Interaction**
```http
POST   /api/v1/clients/tasks/{task_id}/approve          # Approve completed task
POST   /api/v1/clients/tasks/{task_id}/reject           # Reject completed task
POST   /api/v1/clients/tasks/{task_id}/request-revision # Request task revision
GET    /api/v1/clients/tasks/{task_id}/messages         # Get task messages
POST   /api/v1/clients/tasks/{task_id}/message          # Send message to assistant
```

---

## **2. ASSISTANT API ENDPOINTS**

### **Authentication & Profile**
```http
POST   /api/v1/assistants/auth/login          # Assistant login
POST   /api/v1/assistants/auth/logout         # Assistant logout
GET    /api/v1/assistants/profile             # Get assistant profile
PUT    /api/v1/assistants/profile             # Update profile & specialization
POST   /api/v1/assistants/status/online       # Set status to online
POST   /api/v1/assistants/status/offline      # Set status to offline
POST   /api/v1/assistants/auth/refresh-token  # Refresh JWT token
```

### **Task Marketplace**
```http
GET    /api/v1/assistants/tasks/available     # View available tasks to claim
POST   /api/v1/assistants/tasks/{task_id}/claim    # Claim a task
POST   /api/v1/assistants/tasks/{task_id}/release  # Release uncompleted task
```

### **Active Task Management**
```http
GET    /api/v1/assistants/tasks/claimed       # View assistant's active tasks
GET    /api/v1/assistants/tasks/{task_id}     # Get task details + client info
POST   /api/v1/assistants/tasks/{task_id}/complete     # Mark task as completed
POST   /api/v1/assistants/tasks/{task_id}/progress     # Add progress update
POST   /api/v1/assistants/tasks/{task_id}/request-info # Request more info from client
```

### **Communication**
```http
GET    /api/v1/assistants/tasks/{task_id}/client       # Get client contact info
GET    /api/v1/assistants/tasks/{task_id}/messages     # Get task messages
POST   /api/v1/assistants/tasks/{task_id}/message      # Send message to client
POST   /api/v1/assistants/telegram/notify             # Send Telegram message
```

### **Work History & Statistics**
```http
GET    /api/v1/assistants/tasks/completed     # Completed tasks history
GET    /api/v1/assistants/tasks/history       # All task history with filters
GET    /api/v1/assistants/stats/summary       # Performance statistics
GET    /api/v1/assistants/stats/today         # Today's work summary
GET    /api/v1/assistants/stats/month         # Monthly statistics
```

---

## **3. MANAGEMENT API ENDPOINTS**

### **Authentication**
```http
POST   /api/v1/management/auth/login          # Manager login
POST   /api/v1/management/auth/logout         # Manager logout
GET    /api/v1/management/profile             # Get manager profile
POST   /api/v1/management/auth/refresh-token  # Refresh JWT token
```

### **Task Marketplace Control**
```http
GET    /api/v1/management/tasks/marketplace   # View all available tasks
GET    /api/v1/management/tasks/all           # All tasks with filters
GET    /api/v1/management/tasks/overdue       # Tasks past 24h deadline
GET    /api/v1/management/tasks/unclaimed     # Tasks unclaimed >6h
POST   /api/v1/management/tasks/{task_id}/reassign     # Reassign task to different assistant
POST   /api/v1/management/tasks/{task_id}/priority     # Mark task for attention
DELETE /api/v1/management/tasks/{task_id}              # Delete/cancel task
```

### **Assistant Management**
```http
GET    /api/v1/management/assistants          # List all assistants
GET    /api/v1/management/assistants/{id}     # Get assistant details
PUT    /api/v1/management/assistants/{id}     # Update assistant info
POST   /api/v1/management/assistants/{id}/block        # Block assistant
POST   /api/v1/management/assistants/{id}/unblock      # Unblock assistant
GET    /api/v1/management/assistants/performance       # Performance overview
GET    /api/v1/management/assistants/workload          # Workload distribution
```

### **Client Management**
```http
GET    /api/v1/management/clients             # List all clients
GET    /api/v1/management/clients/{id}        # Get client details
PUT    /api/v1/management/clients/{id}        # Update client info
POST   /api/v1/management/clients/{id}/assign-assistant  # Assign dedicated assistant
GET    /api/v1/management/clients/subscriptions         # Subscription overview
GET    /api/v1/management/clients/activity              # Client activity metrics
```

### **Analytics & Reporting**
```http
GET    /api/v1/management/analytics/overview  # Dashboard summary
GET    /api/v1/management/analytics/tasks     # Task completion analytics
GET    /api/v1/management/analytics/assistants # Assistant performance metrics
GET    /api/v1/management/analytics/revenue   # Revenue and subscription analytics
GET    /api/v1/management/analytics/clients   # Client satisfaction metrics
GET    /api/v1/management/analytics/export    # Export analytics data
```

### **Quality Control & Disputes**
```http
GET    /api/v1/management/disputes            # Customer complaints & rejections
GET    /api/v1/management/disputes/{id}       # Get dispute details
POST   /api/v1/management/disputes/{id}/resolve  # Resolve dispute
GET    /api/v1/management/quality/reviews     # Task quality ratings
GET    /api/v1/management/quality/feedback    # Client feedback overview
```

---

## **4. SHARED/COMMON ENDPOINTS**

### **File Management**
```http
POST   /api/v1/upload                         # Upload files/attachments
GET    /api/v1/files/{file_id}                # Download/view uploaded file
DELETE /api/v1/files/{file_id}                # Delete uploaded file
GET    /api/v1/files/{file_id}/metadata       # Get file metadata
```

### **Telegram Integration**
```http
POST   /api/v1/telegram/webhook               # Telegram bot webhook endpoint
POST   /api/v1/telegram/send-message          # Send Telegram notification
POST   /api/v1/telegram/verify-user           # Verify Telegram username
GET    /api/v1/telegram/bot-info              # Get bot information
```

### **System Health**
```http
GET    /api/v1/health                         # API health check
GET    /api/v1/status                         # System status
GET    /api/v1/version                        # API version info
```

---

## **5. WEBSOCKET ENDPOINTS**

### **Real-Time Communication**
```websocket
WS     /ws/clients/{client_id}/tasks          # Client task updates
WS     /ws/assistants/{assistant_id}/tasks    # Assistant marketplace updates  
WS     /ws/management/alerts                  # Management real-time alerts
WS     /ws/tasks/{task_id}/messages           # Task-specific chat messages
```

---

## **6. AUTHENTICATION & AUTHORIZATION**

### **JWT Token Requirements**
```http
# Public endpoints (no auth required)
POST   /api/v1/clients/auth/register
POST   /api/v1/clients/auth/login
POST   /api/v1/assistants/auth/login
POST   /api/v1/management/auth/login
GET    /api/v1/health
GET    /api/v1/status
POST   /api/v1/telegram/webhook

# Protected endpoints (JWT required)
Authorization: Bearer <jwt_token>

# Role-based access control
- client: /api/v1/clients/* endpoints only
- assistant: /api/v1/assistants/* endpoints only  
- manager: /api/v1/management/* endpoints only
- admin: All endpoints
```

---

## **7. HTTP STATUS CODES**

### **Success Responses**
```
200 OK           - Successful GET, PUT, DELETE
201 Created      - Successful POST (resource created)
204 No Content   - Successful DELETE (no response body)
```

### **Client Error Responses**
```
400 Bad Request          - Invalid request data
401 Unauthorized         - Authentication required
403 Forbidden           - Insufficient permissions
404 Not Found           - Resource not found
409 Conflict            - Resource conflict (task already claimed)
422 Unprocessable Entity - Validation errors
429 Too Many Requests   - Rate limit exceeded
```

### **Server Error Responses**
```
500 Internal Server Error - Server error
502 Bad Gateway          - Upstream service error
503 Service Unavailable  - Service temporarily down
```

---

## **8. REQUEST/RESPONSE FORMAT**

### **Standard Response Format**
```json
{
  "success": true|false,
  "data": { ... },           // Success data
  "message": "string",       // Human readable message
  "error": "error_code",     // Error code (if failure)
  "details": { ... },        // Additional error details
  "timestamp": "ISO8601",    // Response timestamp
  "request_id": "uuid"       // Request tracking ID
}
```

### **Pagination Format**
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "total": 150,
    "limit": 20,
    "offset": 40,
    "has_more": true,
    "next_offset": 60
  }
}
```

---

## **9. DATABASE MODELS (Key Entities)**

### **Required Models**
```
- User (clients)
- Assistant  
- Manager
- Task
- Subscription
- Message
- File/Attachment
- TaskAssignment
- TaskHistory
- Rating/Review
```

---

## **10. RATE LIMITING**

### **Rate Limits by Endpoint Type**
```
Authentication endpoints: 5 requests/minute
Task creation: 10 tasks/hour per client
File uploads: 20 uploads/hour per user
General API: 100 requests/minute per user
WebSocket connections: 5 concurrent per user
```

---

## **11. BUSINESS RULES**

### **Task Management Rules**
- All tasks have 24-hour completion deadline from creation
- No priority levels - all tasks are equal priority
- Assistants self-manage their workload capacity
- Business assistants can handle both personal and business tasks
- Personal-only assistants can only handle personal tasks

### **Subscription Model**
- Clients pay monthly subscription fees (no per-task payments)
- Task types restricted by subscription tier:
  - None: No task creation allowed
  - Personal Only: Personal tasks only
  - Business: Business tasks only
  - Full: Both personal and business tasks

### **Assignment Rules**
- Tasks go to marketplace for self-selection by assistants
- Management can manually reassign tasks when needed
- No automatic task assignment or routing

---

## **12. SAMPLE REQUEST/RESPONSE EXAMPLES**

### **Create Task Example**
```http
POST /api/v1/clients/tasks
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "Find dog boarding for weekend",
  "description": "Need pet boarding in downtown area for German Shepherd. Must accept large dogs.",
  "type": "personal"
}
```

### **Response**
```json
{
  "success": true,
  "data": {
    "id": "task_1234",
    "title": "Find dog boarding for weekend",
    "description": "Need pet boarding in downtown area...",
    "type": "personal",
    "status": "pending",
    "created_at": "2024-01-15T10:00:00Z",
    "deadline": "2024-01-16T10:00:00Z",
    "client_id": "12345"
  },
  "message": "Task created successfully. Will be available to assistants shortly.",
  "timestamp": "2024-01-15T10:00:00Z",
  "request_id": "req_abc123"
}
```

---

## **TOTAL ENDPOINT COUNT: 73 ENDPOINTS**
- Client API: 22 endpoints
- Assistant API: 21 endpoints  
- Management API: 26 endpoints
- Shared: 4 endpoints

This specification provides complete coverage for the telegram assistant service platform with subscription-based pricing, self-managed assistant workload, and comprehensive management oversight. 