import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:intl/intl.dart';
import '../providers/task_provider.dart';
import '../models/task.dart';
import '../utils/colors.dart';
import '../widgets/new_task_modal.dart';
import '../widgets/task_detail_modal.dart';

class DashboardSection extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer<TaskProvider>(
      builder: (context, taskProvider, child) {
        return SingleChildScrollView(
          padding: EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  FaIcon(
                    FontAwesomeIcons.tachometerAlt,
                    color: AppColors.primaryBlue,
                    size: 24,
                  ),
                  SizedBox(width: 12),
                  Text(
                    'Мои задачи',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: AppColors.darkGray,
                    ),
                  ),
                ],
              ),
              SizedBox(height: 24),
              Container(
                padding: EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppColors.lightBlue,
                  borderRadius: BorderRadius.circular(12),
                  border: Border(left: BorderSide(color: AppColors.primaryBlue, width: 4)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Текущий план: Стандартный',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: AppColors.primaryBlue,
                      ),
                    ),
                    SizedBox(height: 8),
                    Text(
                      'До 4 задач в день, 5 часов работы',
                      style: TextStyle(color: AppColors.darkGray),
                    ),
                  ],
                ),
              ),
              SizedBox(height: 24),
              Row(
                children: [
                  Expanded(
                    child: _buildStatCard(
                      'Всего', 
                      taskProvider.tasks.length.toString(),
                      AppColors.primaryBlue,
                    ),
                  ),
                  SizedBox(width: 12),
                  Expanded(
                    child: _buildStatCard(
                      'Выполнено', 
                      taskProvider.completedTasks.length.toString(),
                      AppColors.green,
                    ),
                  ),
                ],
              ),
              SizedBox(height: 24),
              if (taskProvider.tasks.isEmpty)
                Center(
                  child: Column(
                    children: [
                      FaIcon(
                        FontAwesomeIcons.clipboard,
                        size: 64,
                        color: AppColors.mediumGray,
                      ),
                      SizedBox(height: 16),
                      Text(
                        'У вас пока нет задач',
                        style: TextStyle(
                          fontSize: 18,
                          color: AppColors.mediumGray,
                        ),
                      ),
                    ],
                  ),
                )
              else
                ...taskProvider.tasks.map((task) => Card(
                  margin: EdgeInsets.only(bottom: 12),
                  child: ListTile(
                    title: Text(task.title),
                    subtitle: Text(task.description),
                    trailing: Chip(
                      label: Text(_getStatusText(task.status)),
                      backgroundColor: _getStatusColor(task.status),
                    ),
                  ),
                )).toList(),
            ],
          ),
        );
      },
    );
  }

  Widget _buildStatCard(String title, String value, Color color) {
    return Container(
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.1),
            blurRadius: 4,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        children: [
          Text(
            value,
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
              color: color,
            ),
          ),
          Text(
            title,
            style: TextStyle(
              fontSize: 14,
              color: AppColors.mediumGray,
            ),
          ),
        ],
      ),
    );
  }

  String _getStatusText(status) {
    switch (status.toString()) {
      case 'TaskStatus.completed': return 'Готово';
      case 'TaskStatus.inProgress': return 'В работе';
      case 'TaskStatus.revision': return 'Доработка';
      default: return 'Ожидает';
    }
  }

  Color _getStatusColor(status) {
    switch (status.toString()) {
      case 'TaskStatus.completed': return AppColors.lightGreen;
      case 'TaskStatus.inProgress': return AppColors.lightYellow;
      case 'TaskStatus.revision': return AppColors.lightRed;
      default: return AppColors.lightBlue;
    }
  }
} 