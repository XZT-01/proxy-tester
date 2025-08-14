import requests

# ASCII art
ASCII_ART = """
▗▄▄▄▄▖▗▄▄▄▖▗▄▄▖▗▄▄▄▖
   ▗▞▘  █  ▐▌ ▐▌ █  
 ▗▞▘    █  ▐▛▀▘  █  
▐▙▄▄▄▖  █  ▐▌    █  
                    
Author: XZT-01
"""

# ANSI color codes for Linux/Termux terminals
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

def check_proxy(proxy: str) -> None:
    """
    Check if a proxy is live by sending a request to httpbin.org.
    Save live proxies to 'LiveProxy.txt'.
    """
    scheme = "http"
    address = proxy

    if "://" in proxy:
        scheme, address = proxy.split("://", 1)

    proxy_dict = {
        "http": f"{scheme}://{address}",
        "https": f"{scheme}://{address}"
    }

    try:
        response = requests.get("https://httpbin.org/ip", proxies=proxy_dict, timeout=5)
        if response.status_code == 200:
            print(f"{Colors.GREEN}[✓] Live: {proxy}{Colors.RESET}")
            with open("LiveProxy.txt", "a") as live_file:
                live_file.write(proxy + "\n")
        else:
            print(f"{Colors.RED}[✗] Dead: {proxy}{Colors.RESET}")
    except requests.RequestException:
        print(f"{Colors.RED}[✗] Dead: {proxy}{Colors.RESET}")

def main() -> None:
    """
    Main function to load proxies from 'proxies.txt' and check them.
    """
    print(ASCII_ART)

    try:
        with open("proxies.txt", "r") as file:
            proxy_list = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{Colors.RED}❌ File 'proxies.txt' not found.{Colors.RESET}")
        return

    print(f"\n{Colors.YELLOW}🔍 Checking {len(proxy_list)} proxies...{Colors.RESET}\n")

    # Clear old live proxies
    open("LiveProxy.txt", "w").close()

    for proxy in proxy_list:
        check_proxy(proxy)

    print(f"\n{Colors.GREEN}✅ Done! Live proxies saved to 'LiveProxy.txt'.{Colors.RESET}")

if __name__ == "__main__":
    main()
