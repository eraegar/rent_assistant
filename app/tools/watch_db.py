#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Monitor Tool for Telegram Assistant
Monitors database changes in real-time
"""

import sqlite3
import time
import os
import sys
from datetime import datetime, timedelta

def get_db_path():
    """Get the correct path to the database file (root/test.db)"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # database is stored in project root/test.db
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
    return os.path.join(project_root, 'test.db')

def get_db_stats():
    """Get comprehensive database statistics"""
    db_path = get_db_path()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        if 'users' not in tables or 'tasks' not in tables:
            return {
                'users_count': 0,
                'tasks_count': 0,
                'users_data': [],
                'tasks_data': [],
                'tables_missing': True,
                'existing_tables': tables,
                'priority_stats': [],
                'type_stats': [],
                'speed_stats': [],
                'tasks_last_24h': 0,
                'avg_tasks_per_user': 0,
                'most_active_user': None
            }
    
        # Get users count
        cursor.execute("SELECT COUNT(*) FROM users")
        users_count = cursor.fetchone()[0]
        
        # Get tasks count
        cursor.execute("SELECT COUNT(*) FROM tasks")
        tasks_count = cursor.fetchone()[0]
        
        # Get all users with task counts
        cursor.execute("""
            SELECT u.id, u.phone, u.name, 
                   COUNT(t.id) as task_count,
                   SUM(CASE WHEN t.status = 'pending' THEN 1 ELSE 0 END) as pending_tasks,
                   SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) as completed_tasks,
                   SUM(CASE WHEN t.status = 'revision' THEN 1 ELSE 0 END) as revision_tasks
            FROM users u 
            LEFT JOIN tasks t ON u.id = t.user_id 
            GROUP BY u.id, u.phone, u.name
            ORDER BY u.id
        """)
        users_data = cursor.fetchall()
        
        # Get all tasks with user info
        cursor.execute("""
            SELECT t.id, t.title, t.type, t.status, t.priority, t.speed,
                   t.created_at, t.completed_at, u.name as user_name, u.phone
            FROM tasks t 
            LEFT JOIN users u ON t.user_id = u.id 
            ORDER BY t.created_at DESC
        """)
        tasks_data = cursor.fetchall()
        
        # Get analytics data
        # Tasks by priority
        cursor.execute("""
            SELECT priority, COUNT(*) as count 
            FROM tasks 
            GROUP BY priority
        """)
        priority_stats = cursor.fetchall()
        
        # Tasks by type
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM tasks 
            GROUP BY type
        """)
        type_stats = cursor.fetchall()
        
        # Tasks by speed
        cursor.execute("""
            SELECT speed, COUNT(*) as count 
            FROM tasks 
            GROUP BY speed
        """)
        speed_stats = cursor.fetchall()
    
        # Recent activity (last 24 hours)
        cursor.execute("""
            SELECT COUNT(*) 
            FROM tasks 
            WHERE datetime(created_at) >= datetime('now', '-1 day')
        """)
        tasks_last_24h = cursor.fetchone()[0]
        
        # Average tasks per user
        cursor.execute("""
            SELECT AVG(task_count) 
            FROM (
                SELECT COUNT(*) as task_count 
                FROM tasks 
                GROUP BY user_id
            )
        """)
        avg_tasks_result = cursor.fetchone()
        avg_tasks_per_user = round(avg_tasks_result[0], 1) if avg_tasks_result[0] else 0
        
        # Most active user
        cursor.execute("""
            SELECT u.name, u.phone, COUNT(t.id) as task_count
            FROM users u
            LEFT JOIN tasks t ON u.id = t.user_id
            GROUP BY u.id, u.name, u.phone
            ORDER BY task_count DESC
            LIMIT 1
        """)
        most_active_user = cursor.fetchone()
    
        return {
            'users_count': users_count,
            'tasks_count': tasks_count,
            'users_data': users_data,
            'tasks_data': tasks_data,
            'priority_stats': priority_stats,
            'type_stats': type_stats,
            'speed_stats': speed_stats,
            'tasks_last_24h': tasks_last_24h,
            'avg_tasks_per_user': avg_tasks_per_user,
            'most_active_user': most_active_user,
            'tables_missing': False,
            'existing_tables': tables
        }
        
    except Exception as e:
        return {
            'users_count': 0,
            'tasks_count': 0,
            'users_data': [],
            'tasks_data': [],
            'error': str(e),
            'tables_missing': True,
            'existing_tables': [],
            'priority_stats': [],
            'type_stats': [],
            'speed_stats': [],
            'tasks_last_24h': 0,
            'avg_tasks_per_user': 0,
            'most_active_user': None
        }
    finally:
        if 'conn' in locals():
            conn.close()

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_db_file_info():
    """Get database file modification info for change tracking"""
    db_path = get_db_path()
    try:
        if not os.path.exists(db_path):
            return {'size': 0, 'modified': 0, 'modified_str': 'Not Found', 'exists': False}
            
        stat = os.stat(db_path)
        return {
            'size': stat.st_size,
            'modified': stat.st_mtime,
            'modified_str': datetime.fromtimestamp(stat.st_mtime).strftime('%H:%M:%S'),
            'exists': True
        }
    except Exception as e:
        return {'size': 0, 'modified': 0, 'modified_str': f'Error: {e}', 'exists': False}

def format_datetime(dt_string):
    """Format datetime string for display"""
    if not dt_string:
        return "N/A"
    try:
        dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        return dt.strftime('%m-%d %H:%M')
    except:
        return dt_string[:16] if len(dt_string) > 16 else dt_string

def main():
    """Main monitoring loop"""
    print("🔍 Database Monitor - Press Ctrl+C to stop")
    print("=" * 50)

    # Track database state
    last_db_state = None

    try:
        while True:
            clear_screen()
            
            # Get current database state
            db_info = get_db_file_info()
            current_time = time.strftime('%H:%M:%S')
            
            # Check for changes
            change_indicator = ""
            if last_db_state and db_info['exists']:
                if db_info['size'] != last_db_state['size']:
                    change_indicator = " 🔄 CHANGED!"
                elif db_info['modified'] != last_db_state['modified']:
                    change_indicator = " 📝 UPDATED!"
            
            print("🔍 DATABASE MONITOR - Live Updates" + change_indicator)
            print("=" * 80)
            
            if not db_info['exists']:
                print(f"⏰ Current Time: {current_time}")
                print("❌ DATABASE FILE NOT FOUND!")
                print(f"   Looking for: {get_db_path()}")
                print("\n💡 Please run the application first to create the database")
            else:
                print(f"⏰ Current Time: {current_time} | 📁 DB Size: {db_info['size']:,} bytes | 🕐 Last Modified: {db_info['modified_str']}")
            
            print()
            
            stats = get_db_stats()
            last_db_state = db_info
            
            if stats.get('tables_missing', False):
                print("⚠️  DATABASE NOT INITIALIZED")
                print(f"   Existing tables: {stats.get('existing_tables', [])}")
                if 'error' in stats:
                    print(f"   Error: {stats['error']}")
                print("\n💡 Run 'python init_db.py' to create tables")
            else:
                print(f"📊 SUMMARY: {stats['users_count']} Users | {stats['tasks_count']} Tasks")
                
                # Users table
                print("\n" + "=" * 80)
                print("👥 USERS TABLE")
                print("=" * 80)
                print(f"{'ID':<4} {'Phone':<15} {'Name':<25} {'Total':<6} {'Pend':<5} {'Done':<5} {'Rev':<4}")
                print("-" * 80)
                
                for user in stats['users_data']:
                    user_id, phone, name, total_tasks, pending, completed, revision = user
                    name = name[:24] if name else "N/A"
                    phone = phone[:14] if phone else "N/A"
                    print(f"{user_id:<4} {phone:<15} {name:<25} {total_tasks:<6} {pending:<5} {completed:<5} {revision:<4}")
                
                if not stats['users_data']:
                    print("   No users found")
                
                # Tasks table
                print("\n" + "=" * 80)
                print("📋 TASKS TABLE")
                print("=" * 80)
                print(f"{'ID':<4} {'Title':<30} {'User':<15} {'Status':<10} {'Priority':<8} {'Type':<8} {'Created':<16}")
                print("-" * 80)
                
                for task in stats['tasks_data']:
                    task_id, title, task_type, status, priority, speed, created_at, completed_at, user_name, phone = task
                    
                    # Format fields
                    title = title[:29] if title else "N/A"
                    user_name = user_name[:14] if user_name else "Unknown"
                    status = status[:9] if status else "N/A"
                    priority = priority[:7] if priority else "N/A"
                    task_type = task_type[:7] if task_type else "N/A"
                    created_str = format_datetime(created_at)
                    
                    # Status icons
                    status_icons = {
                        'pending': '⏳',
                        'completed': '✅',
                        'revision': '🔄'
                    }
                    status_icon = status_icons.get(status, '❓')
                    
                    print(f"{task_id:<4} {title:<30} {user_name:<15} {status_icon}{status:<9} {priority:<8} {task_type:<8} {created_str:<16}")
                
                if not stats['tasks_data']:
                    print("   No tasks found")
                
                # Analytics section
                print("\n" + "=" * 80)
                print("📈 ANALYTICS & STATISTICS")
                print("=" * 80)
                
                # Activity summary
                print(f"🕒 Recent Activity: {stats['tasks_last_24h']} tasks created in last 24h")
                print(f"📊 Average Tasks per User: {stats['avg_tasks_per_user']}")
                
                if stats['most_active_user']:
                    active_name, active_phone, active_count = stats['most_active_user']
                    print(f"🏆 Most Active User: {active_name} ({active_phone}) - {active_count} tasks")
                
                # Priority distribution
                if stats['priority_stats']:
                    print(f"\n🎯 Priority Distribution:")
                    priority_icons = {'high': '🔴', 'medium': '🟡', 'low': '🔵'}
                    for priority, count in stats['priority_stats']:
                        icon = priority_icons.get(priority, '⚪')
                        percentage = (count / stats['tasks_count'] * 100) if stats['tasks_count'] > 0 else 0
                        print(f"   {icon} {priority.capitalize():<8}: {count:>3} tasks ({percentage:>5.1f}%)")
                
                # Type distribution
                if stats['type_stats']:
                    print(f"\n📋 Task Types:")
                    type_icons = {'business': '💼', 'personal': '👤'}
                    for task_type, count in stats['type_stats']:
                        icon = type_icons.get(task_type, '📝')
                        percentage = (count / stats['tasks_count'] * 100) if stats['tasks_count'] > 0 else 0
                        print(f"   {icon} {task_type.capitalize():<10}: {count:>3} tasks ({percentage:>5.1f}%)")
                
                # Speed distribution
                if stats['speed_stats']:
                    print(f"\n⚡ Speed Requirements:")
                    speed_icons = {'urgent': '🚨', 'fast': '⚡', 'standard': '🐌'}
                    for speed, count in stats['speed_stats']:
                        icon = speed_icons.get(speed, '⚪')
                        percentage = (count / stats['tasks_count'] * 100) if stats['tasks_count'] > 0 else 0
                        print(f"   {icon} {speed.capitalize():<10}: {count:>3} tasks ({percentage:>5.1f}%)")
                
                print(f"\n📊 Database Tables: {stats.get('existing_tables', [])}")
                print(f"📁 Database Path: {get_db_path()}")
            
            print("\n" + "=" * 50)
            print("Press Ctrl+C to stop monitoring...")
            
            time.sleep(3)  # Update every 3 seconds
            
    except KeyboardInterrupt:
        print("\n\n✅ Monitoring stopped!")
        print("👋 Thank you for using Database Monitor!")
    except Exception as e:
        print(f"\n\n❌ Error occurred: {e}")
        print("Please check the database configuration and try again.")

if __name__ == "__main__":
    main() 