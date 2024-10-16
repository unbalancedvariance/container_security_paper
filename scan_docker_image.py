import subprocess
import schedule
import time

# Function to scan Docker image using Trivy
def scan_docker_image(image_name):
    try:
        # Run the Trivy scan command for the Docker image
        result = subprocess.run(["trivy", "image", image_name], capture_output=True, text=True)
        
        # Print the result of the scan
        if result.returncode == 0:
            print("Scan completed successfully")
            print(result.stdout)
        else:
            print("Error in scanning")
            print(result.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")

# Schedule the scan every X hours (e.g., every 6 hours)
def schedule_scan(image_name, interval_hours):
    schedule.every(interval_hours).hours.do(scan_docker_image, image_name=image_name)
    
    print(f"Scheduled vulnerability scan for {image_name} every {interval_hours} hours.")
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)

# Example usage
if __name__ == "__main__":
    docker_image_name = "your_docker_image"  # Replace with your Docker image name
    interval = 6  # Set the interval in hours
    schedule_scan(docker_image_name, interval)
