import os
import subprocess

# Input video path
vid = input("Input your video here: ")
if vid.startswith("'"):
    vid = vid[1:-1]  # Strip the surrounding quotes if any.

# Check if the video file exists
if not os.path.exists(vid):
    print("The provided video file doesn't exist!")
    exit()

# Set path for the second script (the one you want to run)
second_script_path = "path_to_second_script.py"  # Change to the location of your second script

# Run the second script with the video file as an argument
try:
    result = subprocess.run(
        ["python", second_script_path, vid],
        capture_output=True, text=True
    )
    
    # Print the output of the second script
    print("Second script output:", result.stdout)
    
    # If there is an error, print the error message
    if result.stderr:
        print("Second script error:", result.stderr)
        
    # Check the return code of the subprocess
    if result.returncode != 0:
        print(f"Error: The second script returned a non-zero exit status: {result.returncode}")
    
except Exception as e:
    print(f"Error running second script: {e}")
