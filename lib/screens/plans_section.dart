import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import '../models/user.dart';
import '../utils/colors.dart';

class PlansSection extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Выберите тарифный план'),
        leading: IconButton(
          icon: Icon(Icons.arrow_back),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            Row(
              children: [
                FaIcon(
                  FontAwesomeIcons.crown,
                  color: AppColors.yellow,
                  size: 24,
                ),
                SizedBox(width: 12),
                Text(
                  'Выберите тарифный план',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: AppColors.darkGray,
                  ),
                ),
              ],
            ),
            SizedBox(height: 24),

            // Plans grid
            ...SubscriptionPlan.values.map((plan) {
              final details = PlanDetails.planDetailsMap[plan]!;
              return Container(
                margin: EdgeInsets.only(bottom: 16),
                child: _buildPlanCard(context, plan, details),
              );
            }).toList(),
          ],
        ),
      ),
    );
  }

  Widget _buildPlanCard(BuildContext context, SubscriptionPlan plan, PlanDetails details) {
    return GestureDetector(
      onTap: () => _selectPlan(context, plan),
      child: Card(
        elevation: details.isPopular ? 8 : 4,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: details.isPopular
              ? BorderSide(color: AppColors.primaryBlue, width: 2)
              : BorderSide.none,
        ),
        child: Container(
          padding: EdgeInsets.all(24),
          child: Column(
            children: [
              // Popular badge
              if (details.isPopular)
                Container(
                  padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: AppColors.primaryBlue,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    'ПОПУЛЯРНЫЙ',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              if (details.isPopular) SizedBox(height: 16),

              // Plan icon
              FaIcon(
                _getPlanIcon(plan),
                color: AppColors.yellow,
                size: 48,
              ),
              SizedBox(height: 16),

              // Plan name
              Text(
                details.name,
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: AppColors.darkGray,
                ),
              ),
              SizedBox(height: 8),

              // Price
              Text(
                details.price,
                style: TextStyle(
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                  color: AppColors.primaryBlue,
                ),
              ),
              Text(
                details.description,
                style: TextStyle(
                  fontSize: 16,
                  color: AppColors.mediumGray,
                ),
              ),
              SizedBox(height: 24),

              // Features
              ...details.features.map((feature) => Padding(
                padding: EdgeInsets.only(bottom: 8),
                child: Row(
                  children: [
                    FaIcon(
                      FontAwesomeIcons.check,
                      color: AppColors.green,
                      size: 16,
                    ),
                    SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        feature,
                        style: TextStyle(
                          fontSize: 16,
                          color: AppColors.darkGray,
                        ),
                      ),
                    ),
                  ],
                ),
              )).toList(),
              SizedBox(height: 24),

              // Select button
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () => _selectPlan(context, plan),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: details.isPopular 
                        ? AppColors.primaryBlue 
                        : AppColors.mediumGray,
                    padding: EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: Text(
                    'Выбрать план',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  IconData _getPlanIcon(SubscriptionPlan plan) {
    switch (plan) {
      case SubscriptionPlan.basic:
        return FontAwesomeIcons.star;
      case SubscriptionPlan.standard:
        return FontAwesomeIcons.starHalfAlt;
      case SubscriptionPlan.premium:
        return FontAwesomeIcons.crown;
    }
  }

  void _selectPlan(BuildContext context, SubscriptionPlan plan) {
    final details = PlanDetails.planDetailsMap[plan]!;
    
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Подтверждение выбора'),
        content: Text('Вы выбрали план "${details.name}" за ${details.price}. Продолжить?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Отмена'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(context); // Close dialog
              Navigator.pop(context); // Go back to main screen
              _showSuccessMessage(context, details);
            },
            child: Text('Подтвердить'),
          ),
        ],
      ),
    );
  }

  void _showSuccessMessage(BuildContext context, PlanDetails details) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('План "${details.name}" успешно выбран!'),
        backgroundColor: AppColors.green,
        duration: Duration(seconds: 3),
      ),
    );
  }
} 