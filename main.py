import os
import time
from threading import Thread

class SimpleOS:
    def __init__(self):
        self.running = True
        self.current_directory = os.getcwd()
        self.processes = {}
        self.process_id = 1

    def shell(self):
        print("Welcome to SimpleOS! Type 'help' for commands.")
        while self.running:
            command = input(f"{self.current_directory} $ ").strip()
            self.execute_command(command)

    def execute_command(self, command):
        if command.startswith("ls"):
            self.list_files()
        elif command.startswith("cd "):
            self.change_directory(command[3:])
        elif command.startswith("mkdir "):
            self.make_directory(command[6:])
        elif command.startswith("rm "):
            self.remove_file(command[3:])
        elif command.startswith("run "):
            self.run_process(command[4:])
        elif command.startswith("fake "):
            self.simple_editor(command[5:])
        elif command.startswith("touch "):
            self.create_file(command[6:])
        elif command == "exit":
            self.shutdown()
        elif command == "help":
            self.show_help()
        else:
            print(f"Unknown command: {command}")

    def list_files(self):
        files = os.listdir(self.current_directory)
        print("\n".join(files) if files else "No files found.")

    def change_directory(self, path):
        try:
            os.chdir(path)
            self.current_directory = os.getcwd()
        except FileNotFoundError:
            print(f"Directory not found: {path}")

    def make_directory(self, name):
        try:
            os.mkdir(name)
            print(f"Directory created: {name}")
        except FileExistsError:
            print(f"Directory already exists: {name}")

    def remove_file(self, name):
        try:
            os.remove(name)
            print(f"File removed: {name}")
        except FileNotFoundError:
            print(f"File not found: {name}")

    def run_process(self, name):
        def dummy_process(pid):
            print(f"Process {pid} started: {name}")
            time.sleep(5)
            print(f"Process {pid} finished.")
            del self.processes[pid]

        pid = self.process_id
        self.process_id += 1
        process_thread = Thread(target=dummy_process, args=(pid,))
        self.processes[pid] = process_thread
        process_thread.start()

    def create_file(self, name):
        try:
            with open(name, 'a'):
                os.utime(name, None)
            print(f"Файл создан: {name}")
        except Exception as e:
            print(f"Ошибка при создании файла: {str(e)}")

    def simple_editor(self, filename):
        print(f"Простой редактор. Введите текст (для завершения введите ':q' на новой строке):")
        content = []
        while True:
            line = input()
            if line == ':q':
                break
            content.append(line)
        
        try:
            with open(filename, 'w') as file:
                file.write('\n'.join(content))
            print(f"Файл сохранен: {filename}")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {str(e)}")

    def show_help(self):
        print("""
SimpleOS Commands:
  ls           - List files in the current directory
  cd <path>    - Change directory
  mkdir <name> - Create a new directory
  rm <name>    - Remove a file
  run <name>   - Run a dummy process
  fake <name>  - Simple text editor
  touch <name> - Create an empty file
  exit         - Shut down the OS
  help         - Show this help message
        """)

    def shutdown(self):
        print("Shutting down SimpleOS...")
        self.running = False
        for process in self.processes.values():
            process.join()
        print("Goodbye!")

if __name__ == "__main__":
    os_system = SimpleOS()
    os_system.shell()