def select_database():
    print("=== ВЫБОР БАЗЫ ДАННЫХ ===\n")
    
    print("1. Данные структурированы?")
    structured = input("Введите 'да' или 'нет': ").lower().strip()
    
    if structured == 'да':
        print("\n2. Данных много?")
        lots_of_data = input("Введите 'да' или 'нет': ").lower().strip()
        
        if lots_of_data == 'да':
            print("\n3. Нагрузка смешанная?")
            mixed_load = input("Введите 'да' или 'нет': ").lower().strip()
            
            if mixed_load == 'да':
                print("\n4. Используются бессерверные вычисления?")
                serverless = input("Введите 'да' или 'нет': ").lower().strip()
                
                if serverless == 'да':
                    return "Yandex Database"
                else:
                    return "MS SQL"
            else:
                print("\n5. Технологии Microsoft?")
                microsoft_tech = input("Введите 'да' или 'нет': ").lower().strip()
                
                if microsoft_tech == 'да':
                    return "MS SQL"
                else:
                    print("\n6. Используется PHP?")
                    php_used = input("Введите 'да' или 'нет': ").lower().strip()
                    
                    if php_used == 'да':
                        return "MySQL"
                    else:
                        return "PostgreSQL"
        else:
            print("\n7. Нужен технологически независимый стек?")
            independent_stack = input("Введите 'да' или 'нет': ").lower().strip()
            
            if independent_stack == 'да':
                print("\n8. Нужна быстрая разработка?")
                fast_development = input("Введите 'да' или 'нет': ").lower().strip()
                
                if fast_development == 'да':
                    print("\n9. Используется PHP?")
                    php_used = input("Введите 'да' или 'нет': ").lower().strip()
                    
                    if php_used == 'да':
                        return "MySQL"
                    else:
                        return "PostgreSQL"
                else:
                    return "PostgreSQL"
            else:
                print("\n10. Технологии Microsoft?")
                microsoft_tech = input("Введите 'да' или 'нет': ").lower().strip()
                
                if microsoft_tech == 'да':
                    return "MS SQL"
                else:
                    print("\n11. Используется PHP?")
                    php_used = input("Введите 'да' или 'нет': ").lower().strip()
                    
                    if php_used == 'да':
                        return "MySQL"
                    else:
                        return "PostgreSQL"
    else:
        print("\n12. Используется стек MEAN?")
        mean_stack = input("Введите 'да' или 'нет': ").lower().strip()
        
        if mean_stack == 'да':
            return "MongoDB"
        else:
            print("\n13. Основная цель - аналитические запросы?")
            analytical_queries = input("Введите 'да' или 'нет': ").lower().strip()
            
            if analytical_queries == 'да':
                print("\n14. Нужен ли полнотекстовый поиск?")
                fulltext_search = input("Введите 'да' или 'нет': ").lower().strip()
                
                if fulltext_search == 'да':
                    print("\n15. Нужно изменять данные?")
                    data_modification = input("Введите 'да' или 'нет': ").lower().strip()
                    
                    if data_modification == 'да':
                        return "Elasticsearch"
                    else:
                        return "ClickHouse"
                else:
                    return "ClickHouse"
            else:
                print("\n16. Есть сложные операции с данными?")
                complex_operations = input("Введите 'да' или 'нет': ").lower().strip()
                
                if complex_operations == 'да':
                    print("\n17. Есть администратор баз данных?")
                    db_administrator = input("Введите 'да' или 'нет': ").lower().strip()
                    
                    if db_administrator == 'да':
                        return "PostgreSQL"
                    else:
                        return "Redis"
                else:
                    return "Redis"


def main():
    result = select_database()
    print(f"\n{'='*50}")
    print(f"РЕКОМЕНДУЕМАЯ БАЗА ДАННЫХ: {result}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
