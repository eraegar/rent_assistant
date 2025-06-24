import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import '../utils/colors.dart';

class WelcomeSection extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Welcome card
          Card(
            elevation: 4,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: Padding(
              padding: EdgeInsets.all(24),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Title
                  Row(
                    children: [
                      FaIcon(
                        FontAwesomeIcons.rocket,
                        color: AppColors.primaryBlue,
                        size: 24,
                      ),
                      SizedBox(width: 12),
                      Text(
                        'Добро пожаловать!',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: AppColors.darkGray,
                        ),
                      ),
                    ],
                  ),
                  SizedBox(height: 16),
                  
                  // Description
                  Text(
                    'Арендуйте персонального ассистента на месяц и делегируйте рутинные задачи. Освободите время для важных дел!',
                    style: TextStyle(
                      fontSize: 16,
                      color: AppColors.mediumGray,
                      height: 1.5,
                    ),
                  ),
                  SizedBox(height: 24),
                  
                  // Benefits grid
                  Row(
                    children: [
                      Expanded(
                        child: _buildBenefitCard(
                          icon: FontAwesomeIcons.clock,
                          title: 'Экономия времени',
                          color: AppColors.primaryBlue,
                          backgroundColor: AppColors.lightBlue,
                        ),
                      ),
                      SizedBox(width: 12),
                      Expanded(
                        child: _buildBenefitCard(
                          icon: FontAwesomeIcons.shieldAlt,
                          title: 'Гарантия качества',
                          color: AppColors.green,
                          backgroundColor: AppColors.lightGreen,
                        ),
                      ),
                    ],
                  ),
                  SizedBox(height: 12),
                  Center(
                    child: _buildBenefitCard(
                      icon: FontAwesomeIcons.users,
                      title: 'Опытные ассистенты',
                      color: AppColors.purple,
                      backgroundColor: AppColors.lightPurple,
                    ),
                  ),
                ],
              ),
            ),
          ),
          SizedBox(height: 24),
          
          // Features section
          Card(
            elevation: 4,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: Padding(
              padding: EdgeInsets.all(24),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Что мы предлагаем',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: AppColors.darkGray,
                    ),
                  ),
                  SizedBox(height: 16),
                  
                  _buildFeatureItem(
                    icon: FontAwesomeIcons.userCog,
                    title: 'Персональный ассистент',
                    description: 'Один выделенный ассистент работает только с вашими задачами',
                  ),
                  SizedBox(height: 12),
                  
                  _buildFeatureItem(
                    icon: FontAwesomeIcons.tasks,
                    title: 'Разные типы задач',
                    description: 'Личные и бизнес задачи любой сложности',
                  ),
                  SizedBox(height: 12),
                  
                  _buildFeatureItem(
                    icon: FontAwesomeIcons.chartLine,
                    title: 'Детальная аналитика',
                    description: 'Отслеживайте прогресс и эффективность выполнения',
                  ),
                  SizedBox(height: 12),
                  
                  _buildFeatureItem(
                    icon: FontAwesomeIcons.mobile,
                    title: 'Удобное приложение',
                    description: 'Управляйте задачами из любого места в любое время',
                  ),
                ],
              ),
            ),
          ),
          SizedBox(height: 100), // Space for FAB
        ],
      ),
    );
  }

  Widget _buildBenefitCard({
    required IconData icon,
    required String title,
    required Color color,
    required Color backgroundColor,
  }) {
    return Container(
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        children: [
          FaIcon(
            icon,
            color: color,
            size: 32,
          ),
          SizedBox(height: 8),
          Text(
            title,
            textAlign: TextAlign.center,
            style: TextStyle(
              fontWeight: FontWeight.w600,
              color: AppColors.darkGray,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildFeatureItem({
    required IconData icon,
    required String title,
    required String description,
  }) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          padding: EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: AppColors.lightBlue,
            borderRadius: BorderRadius.circular(8),
          ),
          child: FaIcon(
            icon,
            color: AppColors.primaryBlue,
            size: 16,
          ),
        ),
        SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                  color: AppColors.darkGray,
                ),
              ),
              SizedBox(height: 4),
              Text(
                description,
                style: TextStyle(
                  fontSize: 14,
                  color: AppColors.mediumGray,
                  height: 1.4,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
} 