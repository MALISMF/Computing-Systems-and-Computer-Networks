def load_vendors(filename: str) -> dict:
    """
    Загружает производителей из файла mac-vendor.txt.
    """
    vendors: dict[str, str] = {}
    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            prefix = parts[0].strip().upper()
            vendor = parts[1].strip()
            if len(prefix) == 6:
                vendors[prefix] = vendor
    return vendors


def normalize_mac_prefix(mac: str) -> str:
    """
    Преобразует MAC-адрес в префикс из 6 шестнадцатеричных символов без разделителей.
      F0-79-59-70-A7-20 -> F07959
      f0:79:59:70:a7:20 -> F07959
    """
    mac = mac.strip().upper()
    # Оставляем только буквы и цифры, убираем разделители ('-', ':', пробелы и т.п.)
    hex_chars = [c for c in mac if c.isalnum()]
    hex_str = "".join(hex_chars)
    if len(hex_str) < 6:
        raise ValueError("Неверный формат MAC-адреса (слишком мало символов).")
    prefix = hex_str[:6]
    # Проверяем, что префикс содержит только шестнадцатеричные символы
    try:
        int(prefix, 16)
    except ValueError:
        raise ValueError("MAC-адрес должен содержать только шестнадцатеричные символы.")
    return prefix


def main() -> None:
    vendors = load_vendors("mac-vendor.txt")

    mac = input("Введите MAC-адрес (например, F0-79-59-70-A7-20): ")
    try:
        prefix = normalize_mac_prefix(mac)
    except ValueError as e:
        print("Ошибка:", e)
        return

    manufacturer = vendors.get(prefix)
    if manufacturer:
        print(f"Производитель: {manufacturer}")
    else:
        print("Производитель для данного MAC-префикса не найден.")


if __name__ == "__main__":
    main()


