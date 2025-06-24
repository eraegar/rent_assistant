import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import '../providers/auth_provider.dart';
import '../utils/colors.dart';
import '../widgets/auth_modal.dart';
import '../widgets/profile_modal.dart';
import '../widgets/new_task_modal.dart';
import 'welcome_section.dart';
import 'dashboard_section.dart';

import 'analytics_section.dart';
import 'plans_section.dart';

class MainScreen extends StatefulWidget {
  @override
  _MainScreenState createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _currentIndex = 0;

  final List<Widget> _sections = [
    WelcomeSection(),
    DashboardSection(),
    AnalyticsSection(),
  ];

  void _showAuthModal() {
    showDialog(
      context: context,
      builder: (context) => AuthModal(),
    );
  }

  void _showProfileModal() {
    showDialog(
      context: context,
      builder: (context) => ProfileModal(),
    );
  }

  void _showPlansSection() {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => PlansSection()),
    );
  }

  void _showNewTaskModal() {
    showDialog(
      context: context,
      builder: (context) => NewTaskModal(),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<AuthProvider>(
      builder: (context, authProvider, child) {
        return Scaffold(
          body: Column(
            children: [
              // Header with gradient background
              Container(
                decoration: BoxDecoration(
                  gradient: AppColors.telegramGradient,
                ),
                child: SafeArea(
                  bottom: false,
                  child: Padding(
                    padding: EdgeInsets.all(16),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Row(
                          children: [
                            FaIcon(
                              FontAwesomeIcons.userTie,
                              color: Colors.white,
                              size: 20,
                            ),
                            SizedBox(width: 8),
                            Text(
                              'Assistant-for-Rent',
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ],
                        ),
                        Row(
                          children: [
                            // Auth/Profile button
                            IconButton(
                              onPressed: authProvider.isAuthenticated
                                  ? _showProfileModal
                                  : _showAuthModal,
                              icon: FaIcon(
                                authProvider.isAuthenticated
                                    ? FontAwesomeIcons.user
                                    : FontAwesomeIcons.signInAlt,
                                color: Colors.white,
                              ),
                            ),
                            // Dashboard button
                            IconButton(
                              onPressed: () => setState(() => _currentIndex = 1),
                              icon: FaIcon(
                                FontAwesomeIcons.tachometerAlt,
                                color: Colors.white,
                              ),
                            ),
                                        // Analytics button
            IconButton(
              onPressed: () => setState(() => _currentIndex = 2),
              icon: FaIcon(
                FontAwesomeIcons.chartBar,
                color: Colors.white,
              ),
            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
              ),
              // Main content
              Expanded(
                child: IndexedStack(
                  index: _currentIndex,
                  children: _sections,
                ),
              ),
            ],
          ),
          // Bottom navigation
          bottomNavigationBar: Container(
            decoration: BoxDecoration(
              border: Border(
                top: BorderSide(color: Colors.grey.shade200),
              ),
            ),
            child: BottomNavigationBar(
              currentIndex: _currentIndex,
              onTap: (index) => setState(() => _currentIndex = index),
              type: BottomNavigationBarType.fixed,
              selectedItemColor: AppColors.primaryBlue,
              unselectedItemColor: Colors.grey,
              items: [
                BottomNavigationBarItem(
                  icon: FaIcon(FontAwesomeIcons.home, size: 20),
                  label: 'Главная',
                ),
                BottomNavigationBarItem(
                  icon: FaIcon(FontAwesomeIcons.tasks, size: 20),
                  label: 'Задачи',
                ),
                BottomNavigationBarItem(
                  icon: FaIcon(FontAwesomeIcons.chartBar, size: 20),
                  label: 'Аналитика',
                ),
              ],
            ),
          ),
          // Floating action button for starting or creating new task
          floatingActionButton: _currentIndex == 0
              ? FloatingActionButton.extended(
                  onPressed: _showPlansSection,
                  backgroundColor: AppColors.primaryBlue,
                  label: Text('Начать работу'),
                  icon: FaIcon(FontAwesomeIcons.rocket, size: 16),
                )
              : _currentIndex == 1
                  ? FloatingActionButton(
                      onPressed: _showNewTaskModal,
                      backgroundColor: AppColors.primaryBlue,
                      child: FaIcon(FontAwesomeIcons.plus),
                    )
                  : null,
        );
      },
    );
  }
} 