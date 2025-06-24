import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import '../providers/task_provider.dart';
import '../models/task.dart';
import '../utils/colors.dart';

class AnalyticsSection extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildHeader(),
          SizedBox(height: 24),
          _buildChartsGrid(),
          SizedBox(height: 80), // Space for bottom navigation
        ],
      ),
    );
  }

  Widget _buildHeader() {
    return Row(
      children: [
        FaIcon(FontAwesomeIcons.chartBar, color: AppColors.green, size: 28),
        SizedBox(width: 12),
        Text(
          'Аналитика',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: AppColors.darkGray,
          ),
        ),
      ],
    );
  }

  Widget _buildChartsGrid() {
    return Consumer<TaskProvider>(
      builder: (context, taskProvider, child) {
        return Column(
          children: [
            Row(
              children: [
                Expanded(child: _buildStatusChart(taskProvider)),
                SizedBox(width: 16),
                Expanded(child: _buildTypeChart(taskProvider)),
              ],
            ),
            SizedBox(height: 16),
            _buildMonthlyChart(taskProvider),
          ],
        );
      },
    );
  }

  Widget _buildStatusChart(TaskProvider taskProvider) {
    final tasks = taskProvider.tasks;
    final completedCount = tasks.where((t) => t.status == TaskStatus.completed).length;
    final pendingCount = tasks.where((t) => t.status == TaskStatus.pending).length;
    final revisionCount = tasks.where((t) => t.status == TaskStatus.revision).length;

    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Статусы задач',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: AppColors.darkGray,
              ),
            ),
            SizedBox(height: 20),
            SizedBox(
              height: 200,
              child: PieChart(
                PieChartData(
                  sections: [
                    PieChartSectionData(
                      value: completedCount.toDouble(),
                      title: 'Выполнено',
                      color: AppColors.green,
                      radius: 60,
                      titleStyle: TextStyle(fontSize: 12, color: Colors.white),
                    ),
                    PieChartSectionData(
                      value: pendingCount.toDouble(),
                      title: 'В работе',
                      color: AppColors.yellow,
                      radius: 60,
                      titleStyle: TextStyle(fontSize: 12, color: Colors.white),
                    ),
                    PieChartSectionData(
                      value: revisionCount.toDouble(),
                      title: 'Доработка',
                      color: AppColors.red,
                      radius: 60,
                      titleStyle: TextStyle(fontSize: 12, color: Colors.white),
                    ),
                  ],
                  centerSpaceRadius: 40,
                  sectionsSpace: 2,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTypeChart(TaskProvider taskProvider) {
    final tasks = taskProvider.tasks;
    final personalCount = tasks.where((t) => t.type == TaskType.personal).length;
    final businessCount = tasks.where((t) => t.type == TaskType.business).length;

    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Типы задач',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: AppColors.darkGray,
              ),
            ),
            SizedBox(height: 20),
            SizedBox(
              height: 200,
              child: BarChart(
                BarChartData(
                  alignment: BarChartAlignment.spaceAround,
                  maxY: (personalCount > businessCount ? personalCount : businessCount).toDouble() + 2,
                  barTouchData: BarTouchData(enabled: false),
                  titlesData: FlTitlesData(
                    show: true,
                    bottomTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        getTitlesWidget: (value, meta) {
                          switch (value.toInt()) {
                            case 0:
                              return Text('Личные', style: TextStyle(fontSize: 12));
                            case 1:
                              return Text('Бизнес', style: TextStyle(fontSize: 12));
                            default:
                              return Text('');
                          }
                        },
                      ),
                    ),
                    leftTitles: AxisTitles(
                      sideTitles: SideTitles(showTitles: false),
                    ),
                    topTitles: AxisTitles(
                      sideTitles: SideTitles(showTitles: false),
                    ),
                    rightTitles: AxisTitles(
                      sideTitles: SideTitles(showTitles: false),
                    ),
                  ),
                  borderData: FlBorderData(show: false),
                  barGroups: [
                    BarChartGroupData(
                      x: 0,
                      barRods: [
                        BarChartRodData(
                          toY: personalCount.toDouble(),
                          color: AppColors.purple,
                          width: 40,
                        ),
                      ],
                    ),
                    BarChartGroupData(
                      x: 1,
                      barRods: [
                        BarChartRodData(
                          toY: businessCount.toDouble(),
                          color: AppColors.blue,
                          width: 40,
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMonthlyChart(TaskProvider taskProvider) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Статистика за последние 7 дней',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: AppColors.darkGray,
              ),
            ),
            SizedBox(height: 20),
            SizedBox(
              height: 200,
              child: LineChart(
                LineChartData(
                  gridData: FlGridData(show: false),
                  titlesData: FlTitlesData(
                    bottomTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        getTitlesWidget: (value, meta) {
                          const days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
                          if (value.toInt() >= 0 && value.toInt() < days.length) {
                            return Text(days[value.toInt()], style: TextStyle(fontSize: 12));
                          }
                          return Text('');
                        },
                      ),
                    ),
                    leftTitles: AxisTitles(
                      sideTitles: SideTitles(showTitles: false),
                    ),
                    topTitles: AxisTitles(
                      sideTitles: SideTitles(showTitles: false),
                    ),
                    rightTitles: AxisTitles(
                      sideTitles: SideTitles(showTitles: false),
                    ),
                  ),
                  borderData: FlBorderData(show: false),
                  lineBarsData: [
                    LineChartBarData(
                      spots: [
                        FlSpot(0, 1),
                        FlSpot(1, 3),
                        FlSpot(2, 2),
                        FlSpot(3, 5),
                        FlSpot(4, 4),
                        FlSpot(5, 6),
                        FlSpot(6, 3),
                      ],
                      isCurved: true,
                      color: AppColors.blue,
                      barWidth: 3,
                      dotData: FlDotData(show: true),
                      belowBarData: BarAreaData(
                        show: true,
                        color: AppColors.blue.withOpacity(0.3),
                      ),
                    ),
                  ],
                  minX: 0,
                  maxX: 6,
                  minY: 0,
                  maxY: 8,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
} 