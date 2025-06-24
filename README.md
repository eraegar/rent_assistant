# Assistant-for-Rent Flutter App

A comprehensive Flutter application for renting personal assistants and managing tasks. This app replicates the functionality of the original HTML web application with a modern, native mobile interface.

## Features

### 🚀 Core Features
- **User Authentication** - Login and registration with phone number
- **Task Management** - Create, view, and manage tasks with different priorities and speeds
- **Subscription Plans** - Choose from Basic, Standard, or Premium plans
- **Analytics Dashboard** - View charts and statistics about task completion
- **Task Examples** - Browse examples of personal and business tasks
- **Real-time Status Updates** - Track task progress and completion

### 📱 Modern UI/UX
- **Material Design** - Clean, modern interface following Flutter design principles
- **Responsive Layout** - Works beautifully on phones and tablets
- **Gradient Header** - Eye-catching blue gradient header
- **Interactive Charts** - Beautiful pie charts and bar charts for analytics
- **Modal Dialogs** - Smooth modal interactions for forms and details
- **Bottom Navigation** - Easy navigation between main sections

### 🎯 Task Management
- **Task Types**: Personal and Business tasks
- **Priority Levels**: Low, Medium, High priority
- **Speed Options**: Standard (24-48h), Fast (6-12h), Urgent (2-4h)
- **Status Tracking**: Pending, In Progress, Completed, Revision
- **Detailed Views** - View full task details with timestamps and results

## Screenshots

The app includes the following main sections:
- **Welcome Screen** - Introduction and app benefits
- **Plans Section** - Subscription plan selection
- **Dashboard** - Task overview with statistics
- **Examples** - Task inspiration and examples
- **Analytics** - Charts and performance metrics

## Getting Started

### Prerequisites
- Flutter SDK (3.0.0 or higher)
- Dart SDK
- Android Studio / VS Code
- Android/iOS device or emulator

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd assistant-for-rent
   ```

2. **Install dependencies**
   ```bash
   flutter pub get
   ```

3. **Run the app**
   ```bash
   flutter run
   ```

### Dependencies

The app uses the following key dependencies:

```yaml
dependencies:
  flutter:
    sdk: flutter
  provider: ^6.0.5          # State management
  http: ^1.1.0              # API calls
  shared_preferences: ^2.2.2 # Local storage
  fl_chart: ^0.64.0         # Charts and analytics
  font_awesome_flutter: ^10.6.0 # Icons
  intl: ^0.18.1             # Date formatting
```

## Architecture

### 📁 Project Structure

```
lib/
├── main.dart                 # App entry point
├── models/                   # Data models
│   ├── task.dart            # Task model with enums
│   └── user.dart            # User and subscription models
├── providers/                # State management
│   ├── auth_provider.dart   # Authentication state
│   └── task_provider.dart   # Task management state
├── screens/                  # Main app screens
│   ├── main_screen.dart     # Main navigation screen
│   ├── welcome_section.dart # Welcome/landing page
│   ├── dashboard_section.dart # Task dashboard
│   ├── examples_section.dart # Task examples
│   ├── analytics_section.dart # Charts and analytics
│   └── plans_section.dart   # Subscription plans
├── widgets/                  # Reusable widgets
│   ├── auth_modal.dart      # Login/register modal
│   ├── profile_modal.dart   # User profile modal
│   ├── new_task_modal.dart  # Create task modal
│   └── task_detail_modal.dart # Task details modal
├── services/                 # External services
│   └── api_service.dart     # Backend API calls
└── utils/                    # Utilities
    └── colors.dart          # App color scheme
```

### 🏗️ State Management

The app uses **Provider** for state management with two main providers:

- **AuthProvider** - Manages user authentication, login/logout, and user data
- **TaskProvider** - Handles task creation, loading, and status updates

### 🎨 Design System

The app follows a consistent design system with:

- **Primary Color**: Blue (#667EEA)
- **Secondary Color**: Purple (#764BA2)
- **Success Color**: Green (#10B981)
- **Warning Color**: Yellow (#F59E0B)
- **Error Color**: Red (#EF4444)

## Features in Detail

### Authentication System
- Phone number-based registration and login
- Form validation with user-friendly error messages
- Persistent login sessions using SharedPreferences
- Mock API implementation (easily replaceable with real backend)

### Task Management
- **Create Tasks**: Rich form with validation
- **Task Types**: Personal or Business categorization
- **Priority System**: Visual indicators for task urgency
- **Speed Selection**: Different completion timeframes with pricing impact
- **Status Tracking**: Visual progress indicators
- **Task Details**: Comprehensive view with all metadata

### Analytics & Charts
- **Pie Charts**: Task status distribution
- **Bar Charts**: Task type comparison
- **Statistics Cards**: Key metrics and KPIs
- **Performance Tracking**: Completion rates and efficiency

### Subscription Management
- **Three Tiers**: Basic, Standard, Premium plans
- **Feature Comparison**: Clear feature lists for each plan
- **Popular Plan Highlighting**: Visual emphasis on recommended plan
- **Plan Selection**: Smooth plan change workflow

## Development Notes

### Mock Data
The app currently uses mock data for demonstration purposes. The `ApiService` class contains mock implementations that can be easily replaced with real API endpoints.

### Responsive Design
The app is designed to work well on various screen sizes, with responsive layouts that adapt to different device dimensions.

### Internationalization
The app is currently in Russian, but the structure supports easy internationalization for other languages.

## Future Enhancements

- [ ] Real backend API integration
- [ ] Push notifications for task updates
- [ ] File attachments for tasks
- [ ] Chat functionality with assistants
- [ ] Payment integration
- [ ] Dark theme support
- [ ] Offline mode capabilities
- [ ] Advanced filtering and search

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions, please open an issue in the repository or contact the development team.

---

**Built with ❤️ using Flutter**

