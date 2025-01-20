import os
import time
import tkinter as tk
from tkinter import ttk
import subprocess
import sys

class TextEditor:
    def __init__(self, filename, parent):
        self.window = tk.Toplevel(parent)
        self.window.title(f"Cheese Editor - {filename}")
        self.window.geometry("600x400")
        
        # Create text area
        self.text_area = tk.Text(self.window, bg='black', fg='white', insertbackground='white')
        self.text_area.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create save button
        self.save_btn = tk.Button(self.window, text="Save", command=lambda: self.save_file(filename))
        self.save_btn.pack(pady=5)
        
        # Load file content if it exists
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                content = file.read()
                self.text_area.insert('1.0', content)
    
    def save_file(self, filename):
        content = self.text_area.get('1.0', 'end-1c')
        with open(filename, 'w') as file:
            file.write(content)
        self.window.title(f"Cheese Editor - {filename} (Saved)")

class SimpleTerminal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple Terminal")
        
        # Configure the main window
        self.root.configure(bg='black')
        self.root.geometry("800x600")
        
        # Create frame for output and input
        self.frame = tk.Frame(self.root, bg='black')
        self.frame.pack(expand=True, fill='both')
        
        # Create text area for output
        self.output = tk.Text(self.frame, bg='black', fg='white', height=20)
        self.output.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create permanent prompt label
        self.prompt_label = tk.Label(self.frame, text="$ ", bg='black', fg='white')
        self.prompt_label.pack(side='left', padx=(5,0))
        
        # Create entry for commands that stays at bottom
        self.command_entry = tk.Entry(self.frame, bg='black', fg='white', insertbackground='white')
        self.command_entry.pack(side='left', fill='x', expand=True, padx=(0,5))
        
        # Keep focus on command entry
        self.command_entry.focus_set()
        self.root.bind('<FocusIn>', lambda e: self.command_entry.focus_set())
        
        # Bind enter key to execute command
        self.command_entry.bind('<Return>', self.execute_command)
        
        # Initialize current directory and editor state
        self.current_dir = os.getcwd()
        self.editing_mode = False
        self.current_file = None
        
        # Show initial prompt
        self.output.insert('1.0', "Simple Terminal v1.0\nType 'help' for available commands\n")
    
    def enter_edit_mode(self, filename):
        self.editing_mode = True
        self.current_file = filename
        self.output.insert('end', f"\nEntering edit mode for {filename}. Type ':q' to quit, ':w' to save.\n")
        self.output.insert('end', "--- Editor Mode ---\n")
        
        # Load file content if it exists
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                content = file.read()
                self.output.insert('end', content)
    
    def save_file(self):
        if not self.current_file:
            return "No file is being edited"
        
        # Get all lines after "--- Editor Mode ---"
        content = self.output.get('1.0', 'end-1c')
        editor_start = content.find("--- Editor Mode ---\n") + len("--- Editor Mode ---\n")
        file_content = content[editor_start:]
        
        try:
            with open(self.current_file, 'w') as file:
                file.write(file_content)
            return f"File {self.current_file} saved successfully"
        except Exception as e:
            return f"Error saving file: {str(e)}"
    
    def run_file(self, filename):
        if not os.path.exists(filename):
            return f"Error: File '{filename}' not found"
        
        try:
            if filename.endswith('.py'):
                process = subprocess.Popen([sys.executable, filename], 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                
                output = stdout.decode()
                errors = stderr.decode()
                
                if output:
                    return f"Output:\n{output}"
                if errors:
                    return f"Errors:\n{errors}"
                return "Program executed successfully with no output"
            else:
                return "Error: Only Python files are supported for now"
        except Exception as e:
            return f"Error running file: {str(e)}"
        
    def execute_command(self, event):
        command = self.command_entry.get()
        
        # Handle editor mode
        if self.editing_mode:
            if command == ':q':
                self.editing_mode = False
                self.current_file = None
                self.output.insert('end', "\nExiting editor mode\n")
            elif command == ':w':
                result = self.save_file()
                self.output.insert('end', f"\n{result}\n")
            else:
                self.output.insert('end', f"{command}\n")
            self.command_entry.delete(0, 'end')
            self.output.see('end')
            return
        
        self.output.insert('end', f"$ {command}\n")
        
        if command == 'exit':
            self.root.quit()
            
        elif command == 'ls':
            try:
                files = os.listdir(self.current_dir)
                for file in files:
                    self.output.insert('end', f"{file}\n")
            except Exception as e:
                self.output.insert('end', f"Error: {str(e)}\n")
                
        elif command.startswith('cd '):
            try:
                new_dir = command[3:]
                os.chdir(new_dir)
                self.current_dir = os.getcwd()
                self.prompt_label.config(text=f"[{os.path.basename(self.current_dir)}]$ ")
            except Exception as e:
                self.output.insert('end', f"Error: {str(e)}\n")
                
        elif command.startswith('mkdir '):
            try:
                dir_name = command[6:]
                os.mkdir(dir_name)
                self.output.insert('end', f"Directory '{dir_name}' created\n")
            except Exception as e:
                self.output.insert('end', f"Error: {str(e)}\n")
                
        elif command.startswith('rmdir '):
            try:
                dir_name = command[6:]
                os.rmdir(dir_name)
                self.output.insert('end', f"Directory '{dir_name}' removed\n")
            except Exception as e:
                self.output.insert('end', f"Error: {str(e)}\n")
                
        elif command.startswith('touch '):
            try:
                file_name = command[6:]
                with open(file_name, 'a'):
                    os.utime(file_name, None)
                self.output.insert('end', f"File '{file_name}' created\n")
            except Exception as e:
                self.output.insert('end', f"Error: {str(e)}\n")
                
        elif command.startswith('rm '):
            try:
                file_name = command[3:]
                os.remove(file_name)
                self.output.insert('end', f"File '{file_name}' removed\n")
            except Exception as e:
                self.output.insert('end', f"Error: {str(e)}\n")
                
        elif command.startswith('edit '):
            try:
                file_name = command[5:]
                self.enter_edit_mode(file_name)
            except Exception as e:
                self.output.insert('end', f"Error: {str(e)}\n")
                
        elif command.startswith('run '):
            try:
                file_name = command[4:]
                result = self.run_file(file_name)
                self.output.insert('end', f"{result}\n")
            except Exception as e:
                self.output.insert('end', f"Error: {str(e)}\n")
                
        elif command == 'help':
            help_text = """Available commands:
- ls: List files in current directory
- cd <path>: Change directory
- mkdir <name>: Create new directory
- rmdir <name>: Remove empty directory
- touch <name>: Create new file
- rm <name>: Remove file
- rename <old> <new>: Rename file or directory
- edit <name>: Edit file in terminal
- run <name>: Run Python file
- clear: Clear terminal output
- exit: Exit the terminal
- help: Show this help message

Editor commands:
- :w  Save file
- :q  Quit editor
"""
            self.output.insert('end', help_text)
            
        elif command == 'clear':
            self.output.delete('1.0', 'end')
            
        elif command.startswith('rename '):
            try:
                # Получаем все после команды 'rename '
                args = command[7:].strip()
                # Находим последний пробел для разделения имен файлов
                split_point = args.rindex(' ')
                old_name = args[:split_point].strip()
                new_name = args[split_point:].strip()
                
                print(f"Debug - Old name: '{old_name}'")  # Отладочный вывод
                print(f"Debug - New name: '{new_name}'")  # Отладочный вывод
                
                # Проверяем существование старого файла
                if not os.path.exists(old_name):
                    self.output.insert('end', f"Error: File '{old_name}' not found\n")
                    return
                    
                # Переименовываем файл
                os.rename(old_name, new_name)
                self.output.insert('end', f"File renamed from '{old_name}' to '{new_name}'\n")
            except Exception as e:
                self.output.insert('end', f"Error: {str(e)}\n")
                
        else:
            self.output.insert('end', f"Unknown command: {command}\n")
        
        # Clear command entry and scroll to bottom
        self.command_entry.delete(0, 'end')
        self.output.see('end')
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    terminal = SimpleTerminal()
    terminal.run()