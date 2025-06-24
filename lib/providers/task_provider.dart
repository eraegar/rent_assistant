import 'package:flutter/material.dart';
import '../models/task.dart';
import '../services/api_service.dart';

class TaskProvider with ChangeNotifier {
  List<Task> _tasks = [];
  bool _isLoading = false;

  List<Task> get tasks => _tasks;
  bool get isLoading => _isLoading;

  List<Task> get completedTasks => _tasks.where((task) => task.status == TaskStatus.completed).toList();
  List<Task> get pendingTasks => _tasks.where((task) => task.status == TaskStatus.pending || task.status == TaskStatus.inProgress).toList();
  List<Task> get revisionTasks => _tasks.where((task) => task.status == TaskStatus.revision).toList();

  final ApiService _apiService = ApiService();

  TaskProvider() {
    loadTasks();
  }

  Future<void> loadTasks() async {
    _setLoading(true);
    try {
      final response = await _apiService.getTasks();
      if (response['success']) {
        _tasks = (response['tasks'] as List)
            .map((taskJson) => Task.fromJson(taskJson))
            .toList();
        notifyListeners();
      }
    } catch (e) {
      print('Error loading tasks: $e');
      // Add some mock data for demo purposes
      _loadMockTasks();
    } finally {
      _setLoading(false);
    }
  }

  Future<bool> createTask({
    required String title,
    required String description,
    required TaskType type,
    required TaskPriority priority,
    required TaskSpeed speed,
  }) async {
    _setLoading(true);
    try {
      final response = await _apiService.createTask(
        title: title,
        description: description,
        type: type,
        priority: priority,
        speed: speed,
      );
      
      if (response['success']) {
        final newTask = Task.fromJson(response['task']);
        _tasks.insert(0, newTask);
        notifyListeners();
        return true;
      }
      return false;
    } catch (e) {
      print('Error creating task: $e');
      // Create mock task for demo
      final newTask = Task(
        id: DateTime.now().millisecondsSinceEpoch.toString(),
        title: title,
        description: description,
        type: type,
        priority: priority,
        speed: speed,
        status: TaskStatus.pending,
        createdAt: DateTime.now(),
      );
      _tasks.insert(0, newTask);
      notifyListeners();
      return true;
    } finally {
      _setLoading(false);
    }
  }

  Future<bool> updateTaskStatus(String taskId, TaskStatus status, {String? result}) async {
    try {
      final response = await _apiService.updateTaskStatus(taskId, status, result: result);
      if (response['success']) {
        final taskIndex = _tasks.indexWhere((task) => task.id == taskId);
        if (taskIndex != -1) {
          // Create a new task with updated status
          final updatedTask = Task(
            id: _tasks[taskIndex].id,
            title: _tasks[taskIndex].title,
            description: _tasks[taskIndex].description,
            type: _tasks[taskIndex].type,
            priority: _tasks[taskIndex].priority,
            speed: _tasks[taskIndex].speed,
            status: status,
            createdAt: _tasks[taskIndex].createdAt,
            completedAt: status == TaskStatus.completed ? DateTime.now() : null,
            result: result ?? _tasks[taskIndex].result,
          );
          _tasks[taskIndex] = updatedTask;
          notifyListeners();
        }
        return true;
      }
      return false;
    } catch (e) {
      print('Error updating task status: $e');
      return false;
    }
  }

  void _loadMockTasks() {
    _tasks = [];
    notifyListeners();
  }

  void _setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }
} 