import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:intl/intl.dart';
import '../models/task.dart';
import '../utils/colors.dart';

class TaskDetailModal extends StatelessWidget {
  final Task task;

  const TaskDetailModal({Key? key, required this.task}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Container(
        width: MediaQuery.of(context).size.width * 0.9,
        constraints: BoxConstraints(maxWidth: 500),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            _buildHeader(context),
            _buildContent(),
            _buildActions(context),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.lightGray,
        borderRadius: BorderRadius.only(
          topLeft: Radius.circular(16),
          topRight: Radius.circular(16),
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            'Детали задачи',
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: AppColors.darkGray,
            ),
          ),
          IconButton(
            onPressed: () => Navigator.pop(context),
            icon: FaIcon(FontAwesomeIcons.times, color: AppColors.mediumGray),
          ),
        ],
      ),
    );
  }

  Widget _buildContent() {
    return Padding(
      padding: EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            task.title,
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: AppColors.darkGray,
            ),
          ),
          SizedBox(height: 8),
          Row(
            children: [
              _buildStatusChip(),
              SizedBox(width: 8),
              _buildTypeChip(),
            ],
          ),
          SizedBox(height: 16),
          Text(
            'Описание:',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: AppColors.darkGray,
            ),
          ),
          SizedBox(height: 8),
          Text(
            task.description,
            style: TextStyle(
              fontSize: 14,
              color: AppColors.mediumGray,
              height: 1.5,
            ),
          ),
          SizedBox(height: 16),
          _buildDetailsGrid(),
          if (task.result != null) ...[
            SizedBox(height: 16),
            Text(
              'Результат:',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: AppColors.darkGray,
              ),
            ),
            SizedBox(height: 8),
            Container(
              padding: EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: AppColors.lightGreen,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text(
                task.result!,
                style: TextStyle(
                  fontSize: 14,
                  color: AppColors.darkGray,
                  height: 1.5,
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildStatusChip() {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: _getStatusColor().withOpacity(0.1),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: _getStatusColor()),
      ),
      child: Text(
        _getStatusText(),
        style: TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.w600,
          color: _getStatusColor(),
        ),
      ),
    );
  }

  Widget _buildTypeChip() {
    final color = task.type == TaskType.business ? AppColors.primaryBlue : AppColors.purple;
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        task.type == TaskType.business ? 'Бизнес' : 'Личное',
        style: TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.w600,
          color: color,
        ),
      ),
    );
  }

  Widget _buildDetailsGrid() {
    return Container(
      padding: EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: AppColors.lightGray,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        children: [
          _buildDetailRow(
            'Приоритет',
            _getPriorityText(),
            FontAwesomeIcons.exclamation,
            _getPriorityColor(),
          ),
          SizedBox(height: 8),
          _buildDetailRow(
            'Скорость',
            _getSpeedText(),
            FontAwesomeIcons.tachometerAlt,
            AppColors.mediumGray,
          ),
          SizedBox(height: 8),
          _buildDetailRow(
            'Создано',
            DateFormat('dd.MM.yyyy HH:mm').format(task.createdAt),
            FontAwesomeIcons.calendar,
            AppColors.mediumGray,
          ),
          if (task.completedAt != null) ...[
            SizedBox(height: 8),
            _buildDetailRow(
              'Завершено',
              DateFormat('dd.MM.yyyy HH:mm').format(task.completedAt!),
              FontAwesomeIcons.checkCircle,
              AppColors.green,
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildDetailRow(String label, String value, IconData icon, Color color) {
    return Row(
      children: [
        FaIcon(icon, size: 16, color: color),
        SizedBox(width: 8),
        Text(
          '$label: ',
          style: TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.w600,
            color: AppColors.darkGray,
          ),
        ),
        Text(
          value,
          style: TextStyle(
            fontSize: 14,
            color: AppColors.mediumGray,
          ),
        ),
      ],
    );
  }

  Widget _buildActions(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(16),
      child: Row(
        children: [
          if (task.status == TaskStatus.completed)
            Expanded(
              child: ElevatedButton.icon(
                onPressed: () => Navigator.pop(context),
                icon: FaIcon(FontAwesomeIcons.check, size: 16),
                label: Text('Принято'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.green,
                ),
              ),
            )
          else ...[
            Expanded(
              child: OutlinedButton.icon(
                onPressed: () => Navigator.pop(context),
                icon: FaIcon(FontAwesomeIcons.redo, size: 16),
                label: Text('На доработку'),
                style: OutlinedButton.styleFrom(
                  side: BorderSide(color: AppColors.red),
                ),
              ),
            ),
            SizedBox(width: 12),
            Expanded(
              child: ElevatedButton.icon(
                onPressed: () => Navigator.pop(context),
                icon: FaIcon(FontAwesomeIcons.check, size: 16),
                label: Text('Принять'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.green,
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }

  Color _getStatusColor() {
    switch (task.status) {
      case TaskStatus.completed:
        return AppColors.green;
      case TaskStatus.inProgress:
      case TaskStatus.pending:
        return AppColors.yellow;
      case TaskStatus.revision:
        return AppColors.red;
    }
  }

  String _getStatusText() {
    switch (task.status) {
      case TaskStatus.completed:
        return 'Выполнено';
      case TaskStatus.inProgress:
        return 'В работе';
      case TaskStatus.pending:
        return 'Ожидает';
      case TaskStatus.revision:
        return 'На доработке';
    }
  }

  String _getPriorityText() {
    switch (task.priority) {
      case TaskPriority.low:
        return 'Обычная';
      case TaskPriority.medium:
        return 'Средняя';
      case TaskPriority.high:
        return 'Высокая';
    }
  }

  Color _getPriorityColor() {
    switch (task.priority) {
      case TaskPriority.low:
        return AppColors.green;
      case TaskPriority.medium:
        return AppColors.yellow;
      case TaskPriority.high:
        return AppColors.red;
    }
  }

  String _getSpeedText() {
    switch (task.speed) {
      case TaskSpeed.standard:
        return 'Стандартная';
      case TaskSpeed.fast:
        return 'Быстрая';
      case TaskSpeed.urgent:
        return 'Срочная';
    }
  }
} 