import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user.dart';
import '../services/api_service.dart';

class AuthProvider with ChangeNotifier {
  User? _user;
  bool _isAuthenticated = false;
  bool _isLoading = false;

  User? get user => _user;
  bool get isAuthenticated => _isAuthenticated;
  bool get isLoading => _isLoading;

  final ApiService _apiService = ApiService();

  AuthProvider() {
    _loadUserFromStorage();
  }

  Future<void> _loadUserFromStorage() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final userJson = prefs.getString('user_data');
      final token = prefs.getString('auth_token');
      
      if (userJson != null && token != null) {
        // In a real app, you'd parse the JSON and create a User object
        _isAuthenticated = true;
        notifyListeners();
      }
    } catch (e) {
      print('Error loading user from storage: $e');
    }
  }

  Future<bool> login(String phone, String password) async {
    _setLoading(true);
    try {
      final response = await _apiService.login(phone, password);
      if (response['success']) {
        await _saveUserData(response['user'], response['token']);
        _user = User.fromJson(response['user']);
        _isAuthenticated = true;
        notifyListeners();
        return true;
      }
      return false;
    } catch (e) {
      print('Login error: $e');
      return false;
    } finally {
      _setLoading(false);
    }
  }

  Future<bool> register(String name, String phone, String password) async {
    _setLoading(true);
    try {
      final response = await _apiService.register(name, phone, password);
      if (response['success']) {
        await _saveUserData(response['user'], response['token']);
        _user = User.fromJson(response['user']);
        _isAuthenticated = true;
        notifyListeners();
        return true;
      }
      return false;
    } catch (e) {
      print('Register error: $e');
      return false;
    } finally {
      _setLoading(false);
    }
  }

  Future<void> logout() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove('user_data');
      await prefs.remove('auth_token');
      
      _user = null;
      _isAuthenticated = false;
      notifyListeners();
    } catch (e) {
      print('Logout error: $e');
    }
  }

  Future<void> _saveUserData(Map<String, dynamic> userData, String token) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('user_data', userData.toString());
      await prefs.setString('auth_token', token);
    } catch (e) {
      print('Error saving user data: $e');
    }
  }

  void _setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }
} 