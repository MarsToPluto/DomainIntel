import socket
import subprocess
import http.client
import ssl
from datetime import datetime

def get_a_record(domain):
    """Fetches the A record (IPv4 address) for a domain."""
    try:
        a_record = socket.gethostbyname(domain)
        return [a_record]
    except socket.gaierror as e:
        return str(e)

def get_aaaa_record(domain):
    """Fetches the AAAA record (IPv6 address) for a domain."""
    try:
        aaaa_record = socket.getaddrinfo(domain, None, socket.AF_INET6)
        return [result[4][0] for result in aaaa_record]
    except socket.gaierror as e:
        return str(e)

def get_nslookup_records(domain, record_type):
    """Uses nslookup to fetch MX, NS, TXT, SOA, and CNAME records."""
    try:
        result = subprocess.run(
            ["nslookup", "-type=" + record_type, domain],
            text=True,
            capture_output=True,
            check=True
        )
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        return str(e)

def get_http_headers(domain):
    """Fetches HTTP headers from the domain."""
    headers = {}
    try:
        conn = http.client.HTTPSConnection(domain, context=ssl.create_default_context())
        conn.request("HEAD", "/")  # Use HEAD request to fetch headers only
        response = conn.getresponse()
        headers = dict(response.getheaders())
    except Exception as e:
        headers['Error'] = str(e)
    finally:
        conn.close()
    
    return headers

def get_ssl_certificate(domain):
    """Fetches SSL certificate information for the domain."""
    cert_info = {}
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                
                # Extracting certificate details
                cert_info['Subject'] = dict(x[0] for x in cert['subject'])
                cert_info['Issuer'] = dict(x[0] for x in cert['issuer'])
                cert_info['Valid From'] = cert['notBefore']
                cert_info['Valid Until'] = cert['notAfter']
                cert_info['Serial Number'] = cert['serialNumber']
                
                # Optional fields
                cert_info['Version'] = cert.get('version', 'N/A')
                cert_info['OCSP'] = cert.get('OCSP', 'N/A')
                
                # Formatting the dates
                cert_info['Valid From'] = datetime.strptime(cert_info['Valid From'], "%b %d %H:%M:%S %Y %Z")
                cert_info['Valid Until'] = datetime.strptime(cert_info['Valid Until'], "%b %d %H:%M:%S %Y %Z")
                
    except Exception as e:
        cert_info['Error'] = str(e)
    
    return cert_info

def get_dns_info(domain):
    """Retrieves DNS information for a domain."""
    dns_info = {}
    
    # A Record
    dns_info['A'] = get_a_record(domain)
    
    # AAAA Record
    dns_info['AAAA'] = get_aaaa_record(domain)
    
    # MX, NS, TXT, SOA, and CNAME records using nslookup
    for record_type in ['MX', 'NS', 'TXT', 'SOA', 'CNAME']:
        dns_info[record_type] = get_nslookup_records(domain, record_type)

    return dns_info

# Main function to display DNS, header, and SSL information
if __name__ == "__main__":
    domain = input("Enter the domain to retrieve DNS, header, and SSL certificate information: ")
    
    # Retrieve and print DNS information
    dns_info = get_dns_info(domain)
    print("DNS Information for domain:", domain)
    for record_type, records in dns_info.items():
        print(f"{record_type} records:")
        for record in records:
            print(record)
        print()
    
    # Retrieve and print HTTP headers
    print("\nHTTP Headers:")
    headers = get_http_headers(domain)
    for header, value in headers.items():
        print(f"{header}: {value}")
    
    # Retrieve and print SSL certificate information
    print("\nSSL Certificate Information:")
    cert_info = get_ssl_certificate(domain)
    for key, value in cert_info.items():
        if isinstance(value, datetime):
            # Format dates for readability
            print(f"{key}: {value.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"{key}: {value}")
