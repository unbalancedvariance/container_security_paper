import json
import subprocess
import time
import logging
from datetime import datetime

# Configure logging
log_file = "configuration_files/audit.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(message)s')

class ZTCAContainerFramework:
    def __init__(self):
        self.image_ids = ["ubuntu"]

    def log(self, message):
        logging.info(message)
        print(message)

    def scan_image(self, image_id):
        try:
            # Run Trivy scan command
            result = subprocess.run(['trivy', 'image', '--format', 'json', image_id],
                                    capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            self.log(f"ZTCF: Error scanning image {image_id}: {e.stderr.strip()}")
            return None

    def process_scan_results(self, results):
        if results and 'Results' in results:
            vulnerabilities_count = {'LOW': 0, 'MEDIUM': 0, 'HIGH': 0}
            for result in results['Results']:
                for vulnerability in result.get('Vulnerabilities', []):
                    severity = vulnerability.get('Severity', 'UNKNOWN').upper()
                    if severity in vulnerabilities_count:
                        vulnerabilities_count[severity] += 1
            
            return vulnerabilities_count
        return None

    def periodic_scan(self, interval=300):
        self.log("ZTCF: ZTCA Container Framework activated.")
        self.log("ZTCF: Continuous monitoring is now enabled.")
        self.log("ZTCF: Periodic image scanning initialized.")

        while True:
            for image_id in self.image_ids:
                scan_results = self.scan_image(image_id)
                vulnerabilities = self.process_scan_results(scan_results)

                if vulnerabilities:
                    log_message = f"ZTCF: [Image Scan - {datetime.now()}] Image ID: {image_id}, Status: Scan Completed, " \
                                  f"Vulnerabilities: {vulnerabilities['LOW']} Low, {vulnerabilities['MEDIUM']} Medium, {vulnerabilities['HIGH']} High."
                    self.log(log_message)
                else:
                    self.log(f"ZTCF: [Image Scan - {datetime.now()}] Image ID: {image_id}, Status: Scan Failed.")

            self.log("ZTCF: End of current monitoring cycle.")
            time.sleep(interval)

if __name__ == "__main__":
    framework = ZTCAContainerFramework()
    framework.periodic_scan()
