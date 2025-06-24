import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import '../utils/colors.dart';

class ExamplesSection extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildHeader(),
          SizedBox(height: 24),
          _buildPersonalTasks(),
          SizedBox(height: 24),
          _buildBusinessTasks(),
          SizedBox(height: 80), // Space for bottom navigation
        ],
      ),
    );
  }

  Widget _buildHeader() {
    return Row(
      children: [
        FaIcon(FontAwesomeIcons.lightbulb, color: AppColors.yellow, size: 28),
        SizedBox(width: 12),
        Text(
          'Примеры задач для вдохновения',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: AppColors.darkGray,
          ),
        ),
      ],
    );
  }

  Widget _buildPersonalTasks() {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                FaIcon(FontAwesomeIcons.user, color: AppColors.purple),
                SizedBox(width: 8),
                Text(
                  'Личные задачи',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: AppColors.purple,
                  ),
                ),
              ],
            ),
            SizedBox(height: 16),
            _buildTaskExample(
              icon: FontAwesomeIcons.pizzaSlice,
              title: 'Заказать пиццу другу, который болеет',
              color: AppColors.purple,
            ),
            _buildTaskExample(
              icon: FontAwesomeIcons.plane,
              title: 'Найти и забронировать семейный тур на выходные',
              color: AppColors.purple,
            ),
            _buildTaskExample(
              icon: FontAwesomeIcons.gift,
              title: 'Выбрать подарок маме на день рождения в бюджете 5000₽',
              color: AppColors.purple,
            ),
            _buildTaskExample(
              icon: FontAwesomeIcons.heart,
              title: 'Организовать сюрприз для жены - букет и доставку',
              color: AppColors.purple,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildBusinessTasks() {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                FaIcon(FontAwesomeIcons.briefcase, color: AppColors.blue),
                SizedBox(width: 8),
                Text(
                  'Бизнес-задачи',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: AppColors.blue,
                  ),
                ),
              ],
            ),
            SizedBox(height: 16),
            _buildTaskExample(
              icon: FontAwesomeIcons.video,
              title: 'Расшифровать запись Zoom-встречи в текстовый формат',
              color: AppColors.blue,
            ),
            _buildTaskExample(
              icon: FontAwesomeIcons.search,
              title: 'Найти контакты 10 потенциальных клиентов в сфере IT',
              color: AppColors.blue,
            ),
            _buildTaskExample(
              icon: FontAwesomeIcons.chartLine,
              title: 'Составить еженедельный отчет по продажам',
              color: AppColors.blue,
            ),
            _buildTaskExample(
              icon: FontAwesomeIcons.calendar,
              title: 'Запланировать встречи с клиентами на следующую неделю',
              color: AppColors.blue,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTaskExample({
    required IconData icon,
    required String title,
    required Color color,
  }) {
    return Container(
      margin: EdgeInsets.only(bottom: 12),
      padding: EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Row(
        children: [
          FaIcon(icon, color: color, size: 20),
          SizedBox(width: 12),
          Expanded(
            child: Text(
              title,
              style: TextStyle(
                fontSize: 14,
                color: AppColors.darkGray,
              ),
            ),
          ),
        ],
      ),
    );
  }
} 