
# EchoDNS

A comprehensive DNS query tool with support for DNS over HTTPS (DoH), AXFR, and reverse lookups.

## Requirements

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Query all DNS records
python echoDNS.py -d example.com

# Query only A records
python echoDNS.py -d example.com -t A

# Query using DNS over HTTPS
python echoDNS.py -d example.com --doh

# Perform a reverse DNS lookup
python echoDNS.py -r 8.8.8.8

# Attempt an AXFR zone transfer
python echoDNS.py -d example.com --axfr -s ns1.example.com
```

### Options:

  * `-d`, `--domain`: The domain(s) to query
  * `-t`, `--type`: DNS record type (e.g., A, MX, CNAME)
  * `-r`, `--reverse`: Perform a reverse DNS lookup (PTR) on an IP address
  * `--doh`: Use DNS over HTTPS
  * `-s`, `--server`: Specify a custom DNS server
  * `--axfr`: Perform an AXFR zone transfer from the specified nameserver
  * `--baseurl`: Base URL for the DoH server

-----

## Making `echoDNS` a Global Command (Linux)

Follow these steps to run the script by just typing `echoDNS` from anywhere in your terminal.

### Step 1: Add the "Shebang" Line

You must edit your `echoDNS.py` file. Add this line as the **very first line** of the script. This tells Linux to use the Python 3 interpreter to run the file.

```python
#!/usr/bin/env python3
```

*(Your file should already have this from our last edit, but it's crucial to check.)*

### Step 2: Make the Script Executable

Navigate to your script's directory and run `chmod` to grant execute permissions.

```bash
chmod +x echoDNS.py
```

### Step 3: Move the Script to a `bin` Directory

The easiest way to make it available system-wide is to move it to `/usr/local/bin` and rename it. This directory is almost always included in your system's `$PATH`.

```bash
sudo mv echoDNS.py /usr/local/bin/echoDNS
```

  * `sudo` is needed because this is a system directory.
  * We rename it from `echoDNS.py` to just `echoDNS` so you don't have to type the `.py` extension.

### Step 4: Run it\!

That's it. Close your current terminal and open a new one (to ensure the `$PATH` is reloaded). You can now run the tool from any directory:

```bash
echoDNS -d google.com
```

```bash
echoDNS -r 1.1.1.1
```