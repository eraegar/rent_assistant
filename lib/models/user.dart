class User {
  final String id;
  final String name;
  final String phone;
  final String email;
  final SubscriptionPlan plan;
  final DateTime createdAt;

  User({
    required this.id,
    required this.name,
    required this.phone,
    required this.email,
    required this.plan,
    required this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      name: json['name'],
      phone: json['phone'],
      email: json['email'] ?? '',
      plan: SubscriptionPlan.values.firstWhere((e) => e.name == json['plan']),
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'phone': phone,
      'email': email,
      'plan': plan.name,
      'created_at': createdAt.toIso8601String(),
    };
  }
}

enum SubscriptionPlan { basic, standard, premium }

class PlanDetails {
  final String name;
  final String price;
  final String description;
  final List<String> features;
  final bool isPopular;

  const PlanDetails({
    required this.name,
    required this.price,
    required this.description,
    required this.features,
    this.isPopular = false,
  });

  static const Map<SubscriptionPlan, PlanDetails> planDetailsMap = {
    SubscriptionPlan.basic: PlanDetails(
      name: 'Базовый',
      price: '15,000₽',
      description: 'в месяц',
      features: [
        '2 часа работы в день',
        '1 задача в день',
        'Персональный ассистент',
        'Базовая аналитика',
      ],
    ),
    SubscriptionPlan.standard: PlanDetails(
      name: 'Стандартный',
      price: '25,000₽',
      description: 'в месяц',
      features: [
        '5 часов работы в день',
        'До 4 задач в день',
        'Персональный ассистент',
        'Расширенная аналитика',
      ],
      isPopular: true,
    ),
    SubscriptionPlan.premium: PlanDetails(
      name: 'Премиум',
      price: '35,000₽',
      description: 'в месяц',
      features: [
        '8 часов работы в день',
        'Неограниченные задачи',
        'Персональный ассистент',
        'Полная аналитика',
      ],
    ),
  };
} 