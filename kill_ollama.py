# import subprocess
# import re

# def run_command(command):
#     try:
#         output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
#         return output.decode('utf-8')
#     except subprocess.CalledProcessError as e:
#         return e.output.decode('utf-8')

# def kill_ollama_processes():
#     # Command to get GPU process information
#     gpu_info_command = "nvidia-smi"
#     gpu_info = run_command(gpu_info_command)

#     # Adjusted regex pattern to accurately capture the process name and PID
#     # This pattern looks for lines where the process name includes 'ollama' and captures the PID
#     pattern = re.compile(r'\|\s+\d+\s+N/A\s+N/A\s+(\d+)\s+\w+\s+.*/ollama\s+\d+MiB\s+\|')

#     # Search for matching processes
#     matches = pattern.findall(gpu_info)
#     if matches:
#         for pid in matches:
#             kill_command = f"sudo kill {pid}"
#             print(f"Killing process with PID: {pid}")
#             result = run_command(kill_command)
#             print(result)
#     else:
#         print("No 'ollama' processes found.")

# if __name__ == "__main__":
#     kill_ollama_processes()




import subprocess
import re

def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.output.decode('utf-8')

def kill_process(pid, password):
    try:
        # Command to kill the process
        command = f"kill {pid}"
        # Use echo to pass the password to sudo -S
        full_command = f"echo {password} | sudo -S {command}"
        subprocess.run(full_command, shell=True, check=True, text=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Process {pid} has been killed.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to kill process {pid}: {e}")

def kill_ollama_processes(password):
    # Command to get GPU process information
    gpu_info_command = "nvidia-smi"
    gpu_info = run_command(gpu_info_command)

    # Adjusted regex pattern to accurately capture the process name and PID
    pattern = re.compile(r'\|\s+\d+\s+N/A\s+N/A\s+(\d+)\s+\w+\s+.*/ollama\s+\d+MiB\s+\|')

    # Search for matching processes
    matches = pattern.findall(gpu_info)
    if matches:
        for pid in matches:
            print(f"Killing process with PID: {pid}")
            kill_process(pid, password)
    else:
        print("No 'ollama' processes found.")

if __name__ == "__main__":
    # Ask for the sudo password
    sudo_password = input("Enter sudo password: ")
    kill_ollama_processes(sudo_password)
