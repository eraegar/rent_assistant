import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/task.dart';

class ApiService {
  static const String baseUrl = 'https://your-api-endpoint.com/api';
  
  // Mock implementation - replace with real API calls
  Future<Map<String, dynamic>> login(String phone, String password) async {
    // Simulate API delay
    await Future.delayed(Duration(seconds: 1));
    
    // Mock successful login
    return {
      'success': true,
      'user': {
        'id': '1',
        'name': 'Иван Петров',
        'phone': phone,
        'email': 'ivan@example.com',
        'plan': 'standard',
        'created_at': DateTime.now().toIso8601String(),
      },
      'token': 'mock_jwt_token_${DateTime.now().millisecondsSinceEpoch}',
    };
  }

  Future<Map<String, dynamic>> register(String name, String phone, String password) async {
    // Simulate API delay
    await Future.delayed(Duration(seconds: 1));

    // Mock successful registration
    return {
      'success': true,
      'user': {
        'id': '1',
        'name': name,
        'phone': phone,
        'email': '',
        'plan': 'basic',
        'created_at': DateTime.now().toIso8601String(),
      },
      'token': 'mock_jwt_token_${DateTime.now().millisecondsSinceEpoch}',
    };
  }

  Future<Map<String, dynamic>> getTasks() async {
    // Simulate API delay
    await Future.delayed(Duration(seconds: 1));

    // Mock tasks data
    return {
      'success': true,
      'tasks': [
        {},
        {},
      ],
    };
  }

  Future<Map<String, dynamic>> createTask({
    required String title,
    required String description,
    required TaskType type,
    required TaskPriority priority,
    required TaskSpeed speed,
  }) async {
    // Simulate API delay
    await Future.delayed(Duration(seconds: 1));
    
    // Mock successful task creation
    return {
      'success': true,
      'task': {
        'id': DateTime.now().millisecondsSinceEpoch.toString(),
        'title': title,
        'description': description,
        'type': type.name,
        'priority': priority.name,
        'speed': speed.name,
        'status': 'pending',
        'created_at': DateTime.now().toIso8601String(),
      },
    };
  }

  Future<Map<String, dynamic>> updateTaskStatus(String taskId, TaskStatus status, {String? result}) async {
    // Simulate API delay
    await Future.delayed(Duration(milliseconds: 500));
    
    // Mock successful update
    return {
      'success': true,
      'message': 'Task status updated successfully',
    };
  }

  // Real API implementation would look like this:
  /*
  Future<Map<String, dynamic>> _makeRequest(String endpoint, {
    String method = 'GET',
    Map<String, dynamic>? body,
  }) async {
    final url = Uri.parse('$baseUrl$endpoint');
    
    final headers = {
      'Content-Type': 'application/json',
      // Add authorization header if needed
      // 'Authorization': 'Bearer $token',
    };

    http.Response response;
    
    switch (method) {
      case 'POST':
        response = await http.post(url, headers: headers, body: jsonEncode(body));
        break;
      case 'PUT':
        response = await http.put(url, headers: headers, body: jsonEncode(body));
        break;
      case 'DELETE':
        response = await http.delete(url, headers: headers);
        break;
      default:
        response = await http.get(url, headers: headers);
    }

    if (response.statusCode >= 200 && response.statusCode < 300) {
      return jsonDecode(response.body);
    } else {
      throw Exception('API request failed: ${response.statusCode}');
    }
  }
  */
} 