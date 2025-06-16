
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor

def ping_ip(ip):
    """Perform ping test and return response time"""
    try:
        # Windows/Linux compatible ping command
        command = ['ping', '-n', '1', ip] if subprocess.os.name == 'nt' else ['ping', '-c', '1', ip]
        output = subprocess.run(command, capture_output=True, text=True, timeout=5)
        
        # Extract ping time
        if match := re.search(r'time=([\d.]+)\s*ms', output.stdout):
            return ip, float(match.group(1))
    except:
        return None
    return None

def read_ips(file_path):
    """Read IP addresses from text file"""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def save_results(results, file_path):
    """Save ping results sorted by response time"""
    # Sort by ping time (ascending)
    sorted_results = sorted(results, key=lambda x: x[1])
    
    with open(file_path, 'w') as f:
        for ip, ping_time in sorted_results:
            f.write(f"{ip}  {int(ping_time)}ms\n")

def main():
    input_file = 'ips.txt'
    output_file = 'ping_results.txt'
    
    print("Reading IP addresses...")
    ips = read_ips(input_file)
    print(f"Found {len(ips)} IPs to test")
    
    print("\nStarting ping tests...")
    successful_pings = []
    
    # Test IPs in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(ping_ip, ips))
    
    # Filter successful pings
    successful_pings = [result for result in results if result]
    
    print(f"\nPing results: {len(successful_pings)} successful, {len(ips)-len(successful_pings)} failed")
    
    # Save sorted results
    save_results(successful_pings, output_file)
    print(f"\nResults saved to {output_file} (sorted by ping time)")

if __name__ == "__main__":
    main()
