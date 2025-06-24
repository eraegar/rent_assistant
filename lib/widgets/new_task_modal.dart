import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import '../providers/task_provider.dart';
import '../models/task.dart';
import '../utils/colors.dart';

class NewTaskModal extends StatefulWidget {
  @override
  _NewTaskModalState createState() => _NewTaskModalState();
}

class _NewTaskModalState extends State<NewTaskModal> {
  final _formKey = GlobalKey<FormState>();
  final _titleController = TextEditingController();
  final _descriptionController = TextEditingController();
  
  TaskType _selectedType = TaskType.personal;
  TaskPriority _selectedPriority = TaskPriority.medium;
  TaskSpeed _selectedSpeed = TaskSpeed.standard;

  @override
  void dispose() {
    _titleController.dispose();
    _descriptionController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Container(
        width: MediaQuery.of(context).size.width * 0.9,
        constraints: BoxConstraints(maxWidth: 500, maxHeight: 600),
        child: Column(
          children: [
            _buildHeader(),
            Expanded(
              child: SingleChildScrollView(
                child: _buildForm(),
              ),
            ),
            _buildActions(),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader() {
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
            'Новая задача',
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

  Widget _buildForm() {
    return Padding(
      padding: EdgeInsets.all(16),
      child: Form(
        key: _formKey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            TextFormField(
              controller: _titleController,
              decoration: InputDecoration(
                labelText: 'Название задачи',
                hintText: 'Опишите задачу кратко',
              ),
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Введите название задачи';
                }
                return null;
              },
            ),
            SizedBox(height: 16),
            TextFormField(
              controller: _descriptionController,
              decoration: InputDecoration(
                labelText: 'Подробное описание',
                hintText: 'Подробно опишите что нужно сделать',
              ),
              maxLines: 4,
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Введите описание задачи';
                }
                return null;
              },
            ),
            SizedBox(height: 16),
            DropdownButtonFormField<TaskType>(
              value: _selectedType,
              decoration: InputDecoration(
                labelText: 'Тип задачи',
                prefixIcon: Icon(Icons.category),
              ),
              items: [
                DropdownMenuItem(
                  value: TaskType.personal,
                  child: Text('Личная'),
                ),
                DropdownMenuItem(
                  value: TaskType.business,
                  child: Text('Бизнес'),
                ),
              ],
              onChanged: (value) {
                setState(() {
                  _selectedType = value!;
                });
              },
            ),
            SizedBox(height: 16),
            DropdownButtonFormField<TaskPriority>(
              value: _selectedPriority,
              decoration: InputDecoration(
                labelText: 'Срочность',
                prefixIcon: Icon(Icons.priority_high),
              ),
              items: [
                DropdownMenuItem(
                  value: TaskPriority.low,
                  child: Text('Обычная'),
                ),
                DropdownMenuItem(
                  value: TaskPriority.medium,
                  child: Text('Средняя'),
                ),
                DropdownMenuItem(
                  value: TaskPriority.high,
                  child: Text('Высокая'),
                ),
              ],
              onChanged: (value) {
                setState(() {
                  _selectedPriority = value!;
                });
              },
            ),
            SizedBox(height: 16),
            DropdownButtonFormField<TaskSpeed>(
              value: _selectedSpeed,
              decoration: InputDecoration(
                labelText: 'Скорость выполнения',
                prefixIcon: Icon(Icons.speed),
              ),
              items: [
                DropdownMenuItem(
                  value: TaskSpeed.standard,
                  child: Text('Стандартная (24-48 часов)'),
                ),
                DropdownMenuItem(
                  value: TaskSpeed.fast,
                  child: Text('Быстрая (6-12 часов) +50%'),
                ),
                DropdownMenuItem(
                  value: TaskSpeed.urgent,
                  child: Text('Срочная (2-4 часа) +100%'),
                ),
              ],
              onChanged: (value) {
                setState(() {
                  _selectedSpeed = value!;
                });
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildActions() {
    return Container(
      padding: EdgeInsets.all(16),
      child: Row(
        children: [
          Expanded(
            child: OutlinedButton.icon(
              onPressed: () => _showPreview(),
              icon: FaIcon(FontAwesomeIcons.eye, size: 16),
              label: Text('Предпросмотр'),
            ),
          ),
          SizedBox(width: 12),
          Expanded(
            child: ElevatedButton.icon(
              onPressed: () => _submitTask(),
              icon: FaIcon(FontAwesomeIcons.paperPlane, size: 16),
              label: Text('Отправить'),
            ),
          ),
        ],
      ),
    );
  }

  void _showPreview() {
    if (_formKey.currentState!.validate()) {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: Text('Предпросмотр задачи'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Название: ${_titleController.text}'),
              SizedBox(height: 8),
              Text('Описание: ${_descriptionController.text}'),
              SizedBox(height: 8),
              Text('Тип: ${_getTypeText(_selectedType)}'),
              SizedBox(height: 8),
              Text('Приоритет: ${_getPriorityText(_selectedPriority)}'),
              SizedBox(height: 8),
              Text('Скорость: ${_getSpeedText(_selectedSpeed)}'),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text('Редактировать'),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.pop(context);
                _submitTask();
              },
              child: Text('Отправить'),
            ),
          ],
        ),
      );
    }
  }

  void _submitTask() async {
    if (_formKey.currentState!.validate()) {
      final taskProvider = Provider.of<TaskProvider>(context, listen: false);
      
      final success = await taskProvider.createTask(
        title: _titleController.text,
        description: _descriptionController.text,
        type: _selectedType,
        priority: _selectedPriority,
        speed: _selectedSpeed,
      );

      if (success) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Задача успешно создана!'),
            backgroundColor: AppColors.green,
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Ошибка при создании задачи'),
            backgroundColor: AppColors.red,
          ),
        );
      }
    }
  }

  String _getTypeText(TaskType type) {
    switch (type) {
      case TaskType.personal:
        return 'Личная';
      case TaskType.business:
        return 'Бизнес';
    }
  }

  String _getPriorityText(TaskPriority priority) {
    switch (priority) {
      case TaskPriority.low:
        return 'Обычная';
      case TaskPriority.medium:
        return 'Средняя';
      case TaskPriority.high:
        return 'Высокая';
    }
  }

  String _getSpeedText(TaskSpeed speed) {
    switch (speed) {
      case TaskSpeed.standard:
        return 'Стандартная';
      case TaskSpeed.fast:
        return 'Быстрая';
      case TaskSpeed.urgent:
        return 'Срочная';
    }
  }
} 