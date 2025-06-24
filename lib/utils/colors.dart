import 'package:flutter/material.dart';

class AppColors {
  static const Color primaryBlue = Color(0xFF667EEA);
  static const Color secondaryPurple = Color(0xFF764BA2);
  static const Color lightGray = Color(0xFFF9FAFB);
  static const Color darkGray = Color(0xFF374151);
  static const Color mediumGray = Color(0xFF6B7280);
  static const Color lightBlue = Color(0xFFEBF8FF);
  static const Color green = Color(0xFF10B981);
  static const Color lightGreen = Color(0xFFF0FDF4);
  static const Color yellow = Color(0xFFF59E0B);
  static const Color lightYellow = Color(0xFFFFFBEB);
  static const Color red = Color(0xFFEF4444);
  static const Color lightRed = Color(0xFFFEF2F2);
  static const Color purple = Color(0xFF8B5CF6);
  static const Color lightPurple = Color(0xFFF5F3FF);
  
  // Additional color aliases for convenience
  static const Color blue = primaryBlue;

  // Gradient for the header
  static const LinearGradient telegramGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [primaryBlue, secondaryPurple],
  );
} 