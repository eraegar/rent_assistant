#!/usr/bin/env python3
"""
Database cleanup utility
Provides functions to safely remove data from the database:
- Delete clients (with their tasks, subscriptions, assignments)
- Delete assistants (with their tasks, assignments)
- Delete managers
- Delete all data (complete cleanup)
"""
import sys
import os
import argparse
from typing import List, Optional

# Добавляем путь к app папке
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(current_dir)
sys.path.append(app_dir)

# Меняем рабочую директорию на app
os.chdir(app_dir)

from database import SessionLocal
from models import (
    User, UserRole, ClientProfile, AssistantProfile, ManagerProfile,
    Task, Subscription, Message, FileAttachment, ClientAssistantAssignment
)
from sqlalchemy import text


def confirm_action(action: str) -> bool:
    """Ask for confirmation before performing destructive action"""
    while True:
        response = input(f"\n⚠️  Are you sure you want to {action}? (type 'yes' to confirm): ").strip().lower()
        if response == 'yes':
            return True
        elif response in ['no', 'n', '']:
            return False
        else:
            print("Please type 'yes' to confirm or 'no' to cancel")


def get_database_stats(db) -> dict:
    """Get current database statistics"""
    stats = {}
    
    # Count users by role
    stats['clients'] = db.query(User).filter(User.role == UserRole.client).count()
    stats['assistants'] = db.query(User).filter(User.role == UserRole.assistant).count()
    stats['managers'] = db.query(User).filter(User.role == UserRole.manager).count()
    stats['total_users'] = db.query(User).count()
    
    # Count other entities
    stats['tasks'] = db.query(Task).count()
    stats['subscriptions'] = db.query(Subscription).count()
    stats['assignments'] = db.query(ClientAssistantAssignment).count()
    stats['messages'] = db.query(Message).count()
    stats['file_attachments'] = db.query(FileAttachment).count()
    
    return stats


def print_database_stats(stats: dict, title: str = "Database Statistics"):
    """Print database statistics in a formatted way"""
    print(f"\n📊 {title}")
    print("=" * 40)
    print(f"👥 Users:")
    print(f"   • Clients: {stats['clients']}")
    print(f"   • Assistants: {stats['assistants']}")
    print(f"   • Managers: {stats['managers']}")
    print(f"   • Total: {stats['total_users']}")
    print(f"📋 Tasks: {stats['tasks']}")
    print(f"💳 Subscriptions: {stats['subscriptions']}")
    print(f"🔗 Assignments: {stats['assignments']}")
    print(f"💬 Messages: {stats['messages']}")
    print(f"📎 File Attachments: {stats['file_attachments']}")
    print("=" * 40)


def delete_clients(db, client_ids: Optional[List[int]] = None) -> int:
    """
    Delete clients and all their related data
    
    Args:
        db: Database session
        client_ids: List of specific client IDs to delete. If None, deletes all clients
    
    Returns:
        Number of clients deleted
    """
    try:
        # Build query for clients to delete
        query = db.query(User).filter(User.role == UserRole.client)
        if client_ids:
            query = query.filter(User.id.in_(client_ids))
        
        clients_to_delete = query.all()
        
        if not clients_to_delete:
            print("No clients found to delete")
            return 0
        
        print(f"\n🔍 Found {len(clients_to_delete)} clients to delete:")
        for client in clients_to_delete:
            print(f"   • {client.name} (ID: {client.id}, Phone: {client.phone})")
        
        if not confirm_action(f"delete {len(clients_to_delete)} clients and ALL their data"):
            print("❌ Operation cancelled")
            return 0
        
        deleted_count = 0
        
        for client in clients_to_delete:
            client_profile = db.query(ClientProfile).filter(ClientProfile.user_id == client.id).first()
            if not client_profile:
                continue
                
            print(f"🗑️  Deleting client: {client.name} (ID: {client.id})")
            
            # Delete messages related to client's tasks
            client_task_ids = db.query(Task.id).filter(Task.client_id == client_profile.id).all()
            if client_task_ids:
                task_ids = [task_id[0] for task_id in client_task_ids]
                messages_deleted = db.query(Message).filter(Message.task_id.in_(task_ids)).delete(synchronize_session=False)
                print(f"   • Deleted {messages_deleted} messages")
                
                # Delete file attachments related to client's tasks
                attachments_deleted = db.query(FileAttachment).filter(FileAttachment.task_id.in_(task_ids)).delete(synchronize_session=False)
                print(f"   • Deleted {attachments_deleted} file attachments")
            
            # Delete client-assistant assignments
            assignments_deleted = db.query(ClientAssistantAssignment).filter(
                ClientAssistantAssignment.client_id == client_profile.id
            ).delete(synchronize_session=False)
            print(f"   • Deleted {assignments_deleted} assistant assignments")
            
            # Delete client's tasks
            tasks_deleted = db.query(Task).filter(Task.client_id == client_profile.id).delete(synchronize_session=False)
            print(f"   • Deleted {tasks_deleted} tasks")
            
            # Delete subscription
            subscription_deleted = db.query(Subscription).filter(Subscription.client_id == client_profile.id).delete(synchronize_session=False)
            print(f"   • Deleted {subscription_deleted} subscriptions")
            
            # Delete client profile
            db.delete(client_profile)
            print(f"   • Deleted client profile")
            
            # Delete user
            db.delete(client)
            print(f"   • Deleted user account")
            
            deleted_count += 1
        
        db.commit()
        print(f"\n✅ Successfully deleted {deleted_count} clients and all their data")
        
        return deleted_count
        
    except Exception as e:
        print(f"\n❌ Error deleting clients: {str(e)}")
        db.rollback()
        return 0


def delete_assistants(db, assistant_ids: Optional[List[int]] = None) -> int:
    """
    Delete assistants and all their related data
    
    Args:
        db: Database session
        assistant_ids: List of specific assistant IDs to delete. If None, deletes all assistants
    
    Returns:
        Number of assistants deleted
    """
    try:
        # Build query for assistants to delete
        query = db.query(User).filter(User.role == UserRole.assistant)
        if assistant_ids:
            query = query.filter(User.id.in_(assistant_ids))
        
        assistants_to_delete = query.all()
        
        if not assistants_to_delete:
            print("No assistants found to delete")
            return 0
        
        print(f"\n🔍 Found {len(assistants_to_delete)} assistants to delete:")
        for assistant in assistants_to_delete:
            print(f"   • {assistant.name} (ID: {assistant.id}, Phone: {assistant.phone})")
        
        if not confirm_action(f"delete {len(assistants_to_delete)} assistants and ALL their data"):
            print("❌ Operation cancelled")
            return 0
        
        deleted_count = 0
        
        for assistant in assistants_to_delete:
            assistant_profile = db.query(AssistantProfile).filter(AssistantProfile.user_id == assistant.id).first()
            if not assistant_profile:
                continue
                
            print(f"🗑️  Deleting assistant: {assistant.name} (ID: {assistant.id})")
            
            # Delete messages related to assistant's tasks
            assistant_task_ids = db.query(Task.id).filter(Task.assistant_id == assistant_profile.id).all()
            if assistant_task_ids:
                task_ids = [task_id[0] for task_id in assistant_task_ids]
                messages_deleted = db.query(Message).filter(Message.task_id.in_(task_ids)).delete(synchronize_session=False)
                print(f"   • Deleted {messages_deleted} messages")
                
                # Delete file attachments related to assistant's tasks
                attachments_deleted = db.query(FileAttachment).filter(FileAttachment.task_id.in_(task_ids)).delete(synchronize_session=False)
                print(f"   • Deleted {attachments_deleted} file attachments")
            
            # Delete client-assistant assignments
            assignments_deleted = db.query(ClientAssistantAssignment).filter(
                ClientAssistantAssignment.assistant_id == assistant_profile.id
            ).delete(synchronize_session=False)
            print(f"   • Deleted {assignments_deleted} client assignments")
            
            # Reset assistant_id to null in tasks (don't delete tasks, just unassign)
            tasks_updated = db.query(Task).filter(Task.assistant_id == assistant_profile.id).update({
                Task.assistant_id: None,
                Task.status: "pending"
            }, synchronize_session=False)
            print(f"   • Unassigned from {tasks_updated} tasks (returned to marketplace)")
            
            # Delete assistant profile
            db.delete(assistant_profile)
            print(f"   • Deleted assistant profile")
            
            # Delete user
            db.delete(assistant)
            print(f"   • Deleted user account")
            
            deleted_count += 1
        
        db.commit()
        print(f"\n✅ Successfully deleted {deleted_count} assistants and all their data")
        
        return deleted_count
        
    except Exception as e:
        print(f"\n❌ Error deleting assistants: {str(e)}")
        db.rollback()
        return 0


def delete_managers(db, manager_ids: Optional[List[int]] = None) -> int:
    """
    Delete managers and their profiles
    
    Args:
        db: Database session
        manager_ids: List of specific manager IDs to delete. If None, deletes all managers
    
    Returns:
        Number of managers deleted
    """
    try:
        # Build query for managers to delete
        query = db.query(User).filter(User.role == UserRole.manager)
        if manager_ids:
            query = query.filter(User.id.in_(manager_ids))
        
        managers_to_delete = query.all()
        
        if not managers_to_delete:
            print("No managers found to delete")
            return 0
        
        print(f"\n🔍 Found {len(managers_to_delete)} managers to delete:")
        for manager in managers_to_delete:
            print(f"   • {manager.name} (ID: {manager.id}, Phone: {manager.phone})")
        
        if not confirm_action(f"delete {len(managers_to_delete)} managers"):
            print("❌ Operation cancelled")
            return 0
        
        deleted_count = 0
        
        for manager in managers_to_delete:
            manager_profile = db.query(ManagerProfile).filter(ManagerProfile.user_id == manager.id).first()
            if manager_profile:
                print(f"🗑️  Deleting manager: {manager.name} (ID: {manager.id})")
                
                # Delete manager profile
                db.delete(manager_profile)
                print(f"   • Deleted manager profile")
                
                # Delete user
                db.delete(manager)
                print(f"   • Deleted user account")
                
                deleted_count += 1
        
        db.commit()
        print(f"\n✅ Successfully deleted {deleted_count} managers")
        
        return deleted_count
        
    except Exception as e:
        print(f"\n❌ Error deleting managers: {str(e)}")
        db.rollback()
        return 0


def delete_all_data(db) -> bool:
    """
    Delete ALL data from the database
    
    Args:
        db: Database session
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print("\n🚨 WARNING: This will DELETE ALL DATA from the database!")
        print("This includes:")
        print("• All users (clients, assistants, managers)")
        print("• All tasks")
        print("• All subscriptions")
        print("• All assignments")
        print("• All messages")
        print("• All file attachments")
        print("• Everything else")
        
        if not confirm_action("DELETE ALL DATA (THIS CANNOT BE UNDONE)"):
            print("❌ Operation cancelled")
            return False
        
        # Double confirmation for safety
        print("\n🔥 FINAL WARNING: You are about to permanently delete ALL data!")
        if not confirm_action("PERMANENTLY DELETE EVERYTHING"):
            print("❌ Operation cancelled")
            return False
        
        print("\n🗑️  Deleting all data...")
        
        # Delete in order due to foreign key constraints
        print("   • Deleting messages...")
        messages_deleted = db.query(Message).delete()
        print(f"     Deleted {messages_deleted} messages")
        
        print("   • Deleting file attachments...")
        attachments_deleted = db.query(FileAttachment).delete()
        print(f"     Deleted {attachments_deleted} file attachments")
        
        print("   • Deleting client-assistant assignments...")
        assignments_deleted = db.query(ClientAssistantAssignment).delete()
        print(f"     Deleted {assignments_deleted} assignments")
        
        print("   • Deleting tasks...")
        tasks_deleted = db.query(Task).delete()
        print(f"     Deleted {tasks_deleted} tasks")
        
        print("   • Deleting subscriptions...")
        subscriptions_deleted = db.query(Subscription).delete()
        print(f"     Deleted {subscriptions_deleted} subscriptions")
        
        print("   • Deleting client profiles...")
        client_profiles_deleted = db.query(ClientProfile).delete()
        print(f"     Deleted {client_profiles_deleted} client profiles")
        
        print("   • Deleting assistant profiles...")
        assistant_profiles_deleted = db.query(AssistantProfile).delete()
        print(f"     Deleted {assistant_profiles_deleted} assistant profiles")
        
        print("   • Deleting manager profiles...")
        manager_profiles_deleted = db.query(ManagerProfile).delete()
        print(f"     Deleted {manager_profiles_deleted} manager profiles")
        
        print("   • Deleting users...")
        users_deleted = db.query(User).delete()
        print(f"     Deleted {users_deleted} users")
        
        # Reset auto-increment sequences (only if sqlite_sequence table exists)
        print("   • Resetting auto-increment sequences...")
        try:
            # Check if sqlite_sequence table exists
            result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence'")).fetchone()
            if result:
                db.execute(text("UPDATE sqlite_sequence SET seq = 0 WHERE name IN ('users', 'client_profiles', 'assistant_profiles', 'manager_profiles', 'tasks', 'subscriptions', 'messages', 'file_attachments', 'client_assistant_assignments')"))
                print("     Auto-increment sequences reset successfully")
            else:
                print("     No auto-increment sequences to reset")
        except Exception as e:
            print(f"     Warning: Could not reset auto-increment sequences: {e}")
        
        db.commit()
        print("\n✅ ALL DATA SUCCESSFULLY DELETED!")
        print("The database is now completely empty.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error deleting all data: {str(e)}")
        db.rollback()
        return False


def interactive_menu():
    """Interactive menu for database cleanup operations"""
    
    db = SessionLocal()
    
    try:
        while True:
            # Show current database stats
            stats = get_database_stats(db)
            print_database_stats(stats)
            
            print("\n🛠️  Database Cleanup Menu")
            print("1. Delete specific clients")
            print("2. Delete ALL clients")
            print("3. Delete specific assistants")
            print("4. Delete ALL assistants")
            print("5. Delete specific managers")
            print("6. Delete ALL managers")
            print("7. Delete ALL data (complete cleanup)")
            print("8. Refresh statistics")
            print("9. Exit")
            
            choice = input("\nSelect an option (1-9): ").strip()
            
            if choice == '1':
                # Delete specific clients
                clients = db.query(User).filter(User.role == UserRole.client).all()
                if not clients:
                    print("No clients found")
                    continue
                    
                print("\nAvailable clients:")
                for client in clients:
                    print(f"  {client.id}: {client.name} ({client.phone})")
                    
                ids_input = input("\nEnter client IDs to delete (comma-separated): ").strip()
                if ids_input:
                    try:
                        client_ids = [int(id.strip()) for id in ids_input.split(',')]
                        delete_clients(db, client_ids)
                    except ValueError:
                        print("❌ Invalid input. Please enter numeric IDs separated by commas.")
                        
            elif choice == '2':
                # Delete ALL clients
                delete_clients(db)
                
            elif choice == '3':
                # Delete specific assistants
                assistants = db.query(User).filter(User.role == UserRole.assistant).all()
                if not assistants:
                    print("No assistants found")
                    continue
                    
                print("\nAvailable assistants:")
                for assistant in assistants:
                    print(f"  {assistant.id}: {assistant.name} ({assistant.phone})")
                    
                ids_input = input("\nEnter assistant IDs to delete (comma-separated): ").strip()
                if ids_input:
                    try:
                        assistant_ids = [int(id.strip()) for id in ids_input.split(',')]
                        delete_assistants(db, assistant_ids)
                    except ValueError:
                        print("❌ Invalid input. Please enter numeric IDs separated by commas.")
                        
            elif choice == '4':
                # Delete ALL assistants
                delete_assistants(db)
                
            elif choice == '5':
                # Delete specific managers
                managers = db.query(User).filter(User.role == UserRole.manager).all()
                if not managers:
                    print("No managers found")
                    continue
                    
                print("\nAvailable managers:")
                for manager in managers:
                    print(f"  {manager.id}: {manager.name} ({manager.phone})")
                    
                ids_input = input("\nEnter manager IDs to delete (comma-separated): ").strip()
                if ids_input:
                    try:
                        manager_ids = [int(id.strip()) for id in ids_input.split(',')]
                        delete_managers(db, manager_ids)
                    except ValueError:
                        print("❌ Invalid input. Please enter numeric IDs separated by commas.")
                        
            elif choice == '6':
                # Delete ALL managers
                delete_managers(db)
                
            elif choice == '7':
                # Delete ALL data
                delete_all_data(db)
                
            elif choice == '8':
                # Refresh statistics (loop will show them)
                continue
                
            elif choice == '9':
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please select 1-9.")
                
            input("\nPress Enter to continue...")
            
    finally:
        db.close()


def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(description='Database cleanup utility')
    parser.add_argument('--interactive', '-i', action='store_true', 
                       help='Run in interactive mode')
    parser.add_argument('--delete-clients', nargs='*', type=int, metavar='ID',
                       help='Delete specific clients by ID (or all if no IDs specified)')
    parser.add_argument('--delete-assistants', nargs='*', type=int, metavar='ID',
                       help='Delete specific assistants by ID (or all if no IDs specified)')
    parser.add_argument('--delete-managers', nargs='*', type=int, metavar='ID',
                       help='Delete specific managers by ID (or all if no IDs specified)')
    parser.add_argument('--delete-all', action='store_true',
                       help='Delete ALL data from database')
    parser.add_argument('--stats', action='store_true',
                       help='Show database statistics only')
    
    args = parser.parse_args()
    
    # If no arguments provided, run interactive mode
    if not any(vars(args).values()):
        interactive_menu()
        return
    
    db = SessionLocal()
    
    try:
        if args.stats:
            stats = get_database_stats(db)
            print_database_stats(stats)
            return
        
        if args.interactive:
            interactive_menu()
            return
            
        if args.delete_all:
            delete_all_data(db)
            return
            
        if args.delete_clients is not None:
            delete_clients(db, args.delete_clients if args.delete_clients else None)
            
        if args.delete_assistants is not None:
            delete_assistants(db, args.delete_assistants if args.delete_assistants else None)
            
        if args.delete_managers is not None:
            delete_managers(db, args.delete_managers if args.delete_managers else None)
            
    finally:
        db.close()


if __name__ == "__main__":
    main() 