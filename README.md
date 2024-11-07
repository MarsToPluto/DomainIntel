
# DomainIntel

**DomainIntel** is a Python-based tool for extracting comprehensive domain information, including DNS records, HTTP headers, and SSL certificate details, all without any third-party libraries. This tool is designed for those who want quick insights into a domain's configuration, security headers, and SSL/TLS certificate status for debugging, verification, or security analysis.

## Features

- **DNS Information**: Fetches A, AAAA, MX, TXT, NS, and CNAME records directly using `socket` and `subprocess` modules.
- **HTTP Headers**: Sends HTTP requests and extracts essential response headers for security insights.
- **SSL Certificate Details**: Retrieves and displays SSL certificate information, including issuer, subject, validity period, and public key.

## Requirements

- Python 3.x
- No additional libraries required!

## Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/MarsToPluto/DomainIntel.git
   cd DomainIntel
   ```

2. Run the script with the desired domain:
   ```bash
   python app.py example.com
   ```

3. **Output**: The script will display:
   - DNS records (A, AAAA, MX, TXT, NS, CNAME)
   - HTTP headers
   - SSL certificate details (if available)

## Example Output

```
Domain: example.com

1. DNS Records:
   - A: 93.184.216.34
   - MX: 10 mail.example.com
   - NS: ns1.example.com, ns2.example.com

2. HTTP Headers:
   - Server: Apache
   - Content-Type: text/html; charset=UTF-8
   - X-Frame-Options: SAMEORIGIN

3. SSL Certificate Info:
   - Issuer: Let's Encrypt Authority X3
   - Subject: CN=example.com
   - Validity: 2024-01-01 to 2024-04-01
```

## Project Structure

- `domainintel.py` – Main script that handles all DNS, HTTP, and SSL queries.
- `README.md` – Project description, usage, and instructions.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more details.
