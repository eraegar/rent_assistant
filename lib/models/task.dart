class Task {
  final String id;
  final String title;
  final String description;
  final TaskType type;
  final TaskPriority priority;
  final TaskSpeed speed;
  final TaskStatus status;
  final DateTime createdAt;
  final DateTime? completedAt;
  final String? result;

  Task({
    required this.id,
    required this.title,
    required this.description,
    required this.type,
    required this.priority,
    required this.speed,
    required this.status,
    required this.createdAt,
    this.completedAt,
    this.result,
  });

  factory Task.fromJson(Map<String, dynamic> json) {
    return Task(
      id: json['id'],
      title: json['title'],
      description: json['description'],
      type: TaskType.values.firstWhere((e) => e.name == json['type']),
      priority: TaskPriority.values.firstWhere((e) => e.name == json['priority']),
      speed: TaskSpeed.values.firstWhere((e) => e.name == json['speed']),
      status: TaskStatus.values.firstWhere((e) => e.name == json['status']),
      createdAt: DateTime.parse(json['created_at']),
      completedAt: json['completed_at'] != null ? DateTime.parse(json['completed_at']) : null,
      result: json['result'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'description': description,
      'type': type.name,
      'priority': priority.name,
      'speed': speed.name,
      'status': status.name,
      'created_at': createdAt.toIso8601String(),
      'completed_at': completedAt?.toIso8601String(),
      'result': result,
    };
  }
}

enum TaskType { personal, business }

enum TaskPriority { low, medium, high }

enum TaskSpeed { standard, fast, urgent }

enum TaskStatus { pending, inProgress, completed, revision } 