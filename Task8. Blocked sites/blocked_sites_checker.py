import re
import socket
import urllib.parse


class BlockedSitesChecker:
    
    def __init__(self, register_file):
        self.entries = []
        self.all_urls = set()
        self.all_domains = set()
        self.all_ips = set()
        
        self._load_register(register_file)
        self._build_indexes()
    
    def _load_register(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                entry = self._parse_line(line)
                if entry:
                    self.entries.append(entry)
    
    def _parse_line(self, line):
        parts = line.split(';')
        if len(parts) != 4:
            return None
        
        date = parts[0].strip()
        urls_str = parts[1].strip()
        domains_str = parts[2].strip()
        ips_str = parts[3].strip()
        
        urls = [url.strip() for url in urls_str.split(',') if url.strip()] if urls_str else []
        domains = [domain.strip() for domain in domains_str.split(',') if domain.strip()] if domains_str else []
        ips = [ip.strip() for ip in ips_str.split(',') if ip.strip()] if ips_str else []
        
        return {
            'date': date,
            'urls': urls,
            'domains': domains,
            'ips': ips
        }
    
    def _build_indexes(self):
        for entry in self.entries:
            for url in entry['urls']:
                self.all_urls.add(url.lower())
            
            for domain in entry['domains']:
                self.all_domains.add(domain.lower())
            
            for ip in entry['ips']:
                self.all_ips.add(ip)
    
    def extract_domain(self, url):
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()
        
        if ':' in domain:
            domain = domain.split(':')[0]
        
        return domain
    
    def get_ip_address(self, domain):
        try:
            ip = socket.gethostbyname(domain)
            return ip
        except:
            return None
    
    def check_url_direct(self, url):
        return url.lower() in self.all_urls
    
    def check_domain(self, url):
        domain = self.extract_domain(url)
        if not domain:
            return False, ""
        
        return domain in self.all_domains, domain
    
    def check_ip(self, domain):
        ip = self.get_ip_address(domain)
        if not ip:
            return False, None
        
        return ip in self.all_ips, ip
    
    def check_site(self, url):
        result = {
            'url': url,
            'blocked': False,
            'reasons': [],
            'details': {}
        }
        
        if self.check_url_direct(url):
            result['blocked'] = True
            result['reasons'].append("URL найден в реестре запрещенных")
            result['details']['direct_url_match'] = True
        
        domain_blocked, domain = self.check_domain(url)
        if domain_blocked:
            result['blocked'] = True
            result['reasons'].append(f"Домен '{domain}' найден в реестре запрещенных")
            result['details']['domain_match'] = True
            result['details']['blocked_domain'] = domain
        
        if domain:
            ip_blocked, ip = self.check_ip(domain)
            if ip_blocked:
                result['blocked'] = True
                result['reasons'].append(f"IP адрес '{ip}' найден в реестре запрещенных")
                result['details']['ip_match'] = True
                result['details']['blocked_ip'] = ip
            elif ip:
                result['details']['resolved_ip'] = ip
        
        return result
    
    def get_statistics(self):
        return {
            'total_entries': len(self.entries),
            'total_urls': len(self.all_urls),
            'total_domains': len(self.all_domains),
            'total_ips': len(self.all_ips)
        }


def main():
    print("=" * 50)
    print("    ПРОВЕРКА ЗАБЛОКИРОВАННЫХ САЙТОВ")
    print("=" * 50)
    
    checker = BlockedSitesChecker('register.txt')
    stats = checker.get_statistics()
    
    print(f"Загружено: {stats['total_entries']} записей")
    print(f"URL: {stats['total_urls']}, Доменов: {stats['total_domains']}, IP: {stats['total_ips']}")
    print("=" * 50)
    
    while True:
        url = input("URL: ").strip()
        
        if url.lower() in ['quit', 'exit', 'выход']:
            break
        
        if not url:
            continue
        
        result = checker.check_site(url)
        
        print(f"Проверка: {url}")
        
        if result['blocked']:
            print("Результат: ЗАБЛОКИРОВАН")
            print("Причины:")
            for reason in result['reasons']:
                print(f"  • {reason}")
        else:
            print("Результат: СВОБОДЕН")
        
        if 'resolved_ip' in result['details']:
            print(f"IP адрес: {result['details']['resolved_ip']}")
        
        print("=" * 40)


if __name__ == "__main__":
    main()
