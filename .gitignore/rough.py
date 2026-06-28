import dns.resolver 
from urllib.parse import urlparse

answers = dns.resolver.resolve("chatgpt.com", "A")
print(answers)
for record in answers:
    print(record.address)
ips = [record.address for record in answers]
print(ips)