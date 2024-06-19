import os

def clean_migrations(project_root):
    for root, dirs, files in os.walk(project_root):
        if 'migrations' in dirs:
            migrations_path = os.path.join(root, 'migrations')
            for file_name in os.listdir(migrations_path):
                if file_name != '__init__.py' and file_name.endswith('.py'):
                    file_path = os.path.join(migrations_path, file_name)
                    print(f"Removing file: {file_path}")
                    os.remove(file_path)

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    clean_migrations(project_root)
    print("Migration files cleaned up successfully.")
