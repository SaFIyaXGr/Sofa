
import sqlite3

# Путь к файлу базы данных
DATABASE_FILE = 'insurance_company.db'

def create_database():
    """Создает базу данных и таблицы."""
    conn = None  # Ensure conn is defined even if connection fails
    try:
        # 1. Подключение к базе данных (создаст файл, если его нет)
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # 2. Создание таблиц (используем многострочные строки для удобства)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Clients (
                ClientID INTEGER PRIMARY KEY AUTOINCREMENT,  -- SQLite uses INTEGER PRIMARY KEY AUTOINCREMENT
                ClientType VARCHAR(50),
                FullName VARCHAR(255) NOT NULL,
                DateOfBirth DATE,
                Gender CHAR(1),
                Address VARCHAR(255),
                PhoneNumber VARCHAR(20),
                Email VARCHAR(255),
                RegistrationDate DATE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS InsuranceProducts (
                ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
                ProductName VARCHAR(255) NOT NULL,
                ProductDescription TEXT,
                CoverageDetails TEXT,
                PremiumCalculationMethod VARCHAR(255)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Policies (
                PolicyID INTEGER PRIMARY KEY AUTOINCREMENT,
                ClientID INT,
                ProductID INT,
                PolicyNumber VARCHAR(255),
                IssueDate DATE,
                ExpiryDate DATE,
                PremiumAmount DECIMAL(10, 2),
                PolicyStatus VARCHAR(50),
                FOREIGN KEY (ClientID) REFERENCES Clients(ClientID),
                FOREIGN KEY (ProductID) REFERENCES InsuranceProducts(ProductID)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Claims (
                ClaimID INTEGER PRIMARY KEY AUTOINCREMENT,
                PolicyID INT,
                ClaimDate DATE,
                LossDescription TEXT,
                ClaimAmount DECIMAL(10, 2),
                ClaimStatus VARCHAR(50),
                FOREIGN KEY (PolicyID) REFERENCES Policies(PolicyID)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Payments (
                PaymentID INTEGER PRIMARY KEY AUTOINCREMENT,
                ClientID INT,
                PolicyID INT,
                PaymentDate DATE,
                PaymentAmount DECIMAL(10, 2),
                PaymentMethod VARCHAR(50),
                FOREIGN KEY (ClientID) REFERENCES Clients(ClientID),
                FOREIGN KEY (PolicyID) REFERENCES Policies(PolicyID)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Agents (
                AgentID INTEGER PRIMARY KEY AUTOINCREMENT,
                FullName VARCHAR(255) NOT NULL,
                PhoneNumber VARCHAR(20),
                Email VARCHAR(255),
                CommissionRate DECIMAL(5, 2)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS UserAccounts (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Username VARCHAR(255) NOT NULL UNIQUE,
                PasswordHash VARCHAR(255) NOT NULL,
                Role VARCHAR(50),
                Email VARCHAR(255),
                LastLogin DATETIME
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS AuditLog (
                LogID INTEGER PRIMARY KEY AUTOINCREMENT,
                Timestamp DATETIME,
                UserID INT,
                Action VARCHAR(255),
                TableName VARCHAR(255),
                RecordID INT,
                FOREIGN KEY (UserID) REFERENCES UserAccounts(UserID)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS SystemSettings (
                SettingID INTEGER PRIMARY KEY AUTOINCREMENT,
                SettingName VARCHAR(255) UNIQUE,
                SettingValue VARCHAR(255)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ClaimDocuments (
                DocumentID INTEGER PRIMARY KEY AUTOINCREMENT,
                ClaimID INT,
                DocumentType VARCHAR(255),
                FilePath VARCHAR(255),
                UploadDate DATETIME,
                FOREIGN KEY (ClaimID) REFERENCES Claims(ClaimID)
            )
        """)

        # 3. Сохранение изменений
        conn.commit()
        print("База данных и таблицы успешно созданы.")

    except sqlite3.Error as e:
        print(f"Ошибка при создании базы данных: {e}")
    finally:
        if conn:
            conn.close()

def fill_tables():
    """Заполняет таблицы тестовыми данными."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # Заполнение таблицы Clients (Клиенты)
        cursor.execute("""
            INSERT INTO Clients (ClientType, FullName, DateOfBirth, Gender, Address, PhoneNumber, Email, RegistrationDate) VALUES
            ('Individual', 'Иванов Иван Иванович', '1985-03-15', 'M', 'Москва, ул. Ленина, д. 1', '+79161234567', 'ivanov@example.com', '2023-10-20'),
            ('Corporate', 'ООО "Ромашка"', '2010-07-01', NULL, 'Москва, ул. Строителей, д. 5', '+74957778899', 'info@romashka.ru', '2023-09-10'),
            ('Individual', 'Петрова Анна Сергеевна', '1992-11-20', 'F', 'Санкт-Петербург, Невский пр., д. 10', '+79219876543', 'petrova@example.com', '2023-10-25');
        """)

        # Заполнение таблицы InsuranceProducts (Страховые продукты)
        cursor.execute("""
            INSERT INTO InsuranceProducts (ProductName, ProductDescription, CoverageDetails, PremiumCalculationMethod) VALUES
            ('КАСКО', 'Страхование автотранспорта от ущерба и хищения', 'Покрытие ущерба в результате ДТП, стихийных бедствий, противоправных действий третьих лиц, угона', 'На основе возраста, стажа вождения, стоимости автомобиля'),
            ('ОСАГО', 'Обязательное страхование гражданской ответственности владельцев транспортных средств', 'Покрытие ущерба, причиненного третьим лицам в результате ДТП по вине страхователя', 'На основе возраста, стажа вождения, региона регистрации автомобиля'),
            ('Страхование жизни', 'Страхование жизни и здоровья от несчастных случаев', 'Выплата страховой суммы в случае смерти, инвалидности или травмы в результате несчастного случая', 'На основе возраста, пола, профессии, состояния здоровья');
        """)

        # Заполнение таблицы Policies (Полисы)
        cursor.execute("""
            INSERT INTO Policies (ClientID, ProductID, PolicyNumber, IssueDate, ExpiryDate, PremiumAmount, PolicyStatus) VALUES
            (1, 1, 'POL-001', '2023-10-27', '2024-10-27', 15000.00, 'Active'),
            (2, 2, 'POL-002', '2023-10-28', '2024-10-28', 5000.00, 'Active'),
            (3, 3, 'POL-003', '2023-10-29', '2024-10-29', 20000.00, 'Active');
        """)

        # Заполнение таблицы Claims (Страховые случаи)
        cursor.execute("""
            INSERT INTO Claims (PolicyID, ClaimDate, LossDescription, ClaimAmount, ClaimStatus) VALUES
            (1, '2023-11-05', 'ДТП - столкновение с другим автомобилем', 50000.00, 'Open'),
            (2, '2023-11-06', 'Повреждение стекла камнем', 2000.00, 'Approved');
        """)

        # Заполнение таблицы Payments (Платежи)
        cursor.execute("""
            INSERT INTO Payments (ClientID, PolicyID, PaymentDate, PaymentAmount, PaymentMethod) VALUES
            (1, 1, '2023-10-27', 15000.00, 'Банковская карта'),
            (2, 2, '2023-10-28', 5000.00, 'Наличные'),
            (3, 3, '2023-10-29', 20000.00, 'Банковский перевод');
        """)

        # Заполнение таблицы Agents (Агенты)
        cursor.execute("""
            INSERT INTO Agents (FullName, PhoneNumber, Email, CommissionRate) VALUES
            ('Смирнов Алексей Петрович', '+79031112233', 'smirnov@example.com', 0.10),
            ('Кузнецова Елена Ивановна', '+79154445566', 'kuznetsova@example.com', 0.12);
        """)

        # Заполнение таблицы UserAccounts (Учётные записи пользователей)
        cursor.execute("""
            INSERT INTO UserAccounts (Username, PasswordHash, Role, Email, LastLogin) VALUES
            ('admin', 'hashed_password_admin', 'Administrator', 'admin@example.com', '2023-11-06 10:00:00'),
            ('agent1', 'hashed_password_agent1', 'Agent', 'agent1@example.com', '2023-11-06 11:00:00');
        """)

        # Заполнение таблицы AuditLog (Журнал аудита)
        cursor.execute("""
            INSERT INTO AuditLog (Timestamp, UserID, Action, TableName, RecordID) VALUES
            ('2023-11-06 12:00:00', 1, 'Created new client', 'Clients', 1),
            ('2023-11-06 13:00:00', 2, 'Updated policy status', 'Policies', 2);
        """)

        # Заполнение таблицы SystemSettings (Системные настройки)
        cursor.execute("""
            INSERT INTO SystemSettings (SettingName, SettingValue) VALUES
            ('DefaultCurrency', 'RUB'),
            ('ReportLogoPath', '/images/logo.png');
        """)

        # Заполнение таблицы ClaimDocuments (Документы по страховым случаям)
        cursor.execute("""
            INSERT INTO ClaimDocuments (ClaimID, DocumentType, FilePath, UploadDate) VALUES
            (1, 'Заявление о страховом случае', '/documents/claim1_statement.pdf', '2023-11-05 14:30:00'),
            (1, 'Справка из полиции', '/documents/claim1_police_report.pdf', '2023-11-05 15:00:00');
        """)

        conn.commit()
        print("Таблицы успешно заполнены тестовыми данными.")

    except sqlite3.Error as e:
        print(f"Ошибка при заполнении таблиц: {e}")
    finally:
        if conn:
            conn.close()

def test_queries():
    """Выполняет тестовые запросы и выводит результаты."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # 12 Тестовых запросов
        queries = [
            ("1. Выбрать всех клиентов", "SELECT * FROM Clients"),
            ("2. Выбрать страховые продукты с названием, содержащим 'Страхование'", "SELECT * FROM InsuranceProducts WHERE ProductName LIKE '%Страхование%'"),
            ("3. Выбрать полисы, выданные в 2023 году", "SELECT * FROM Policies WHERE strftime('%Y', IssueDate) = '2023'"),
            ("4. Выбрать страховые случаи со статусом 'Open'", "SELECT * FROM Claims WHERE ClaimStatus = 'Open'"),
            ("5. Выбрать платежи, совершенные банковской картой", "SELECT * FROM Payments WHERE PaymentMethod = 'Банковская карта'"),
            ("6. Выбрать агентов с комиссией выше 10%", "SELECT * FROM Agents WHERE CommissionRate > 0.10"),
            ("7. Выбрать пользователей с ролью 'Administrator'", "SELECT * FROM UserAccounts WHERE Role = 'Administrator'"),
            ("8. Выбрать последние 5 записей из журнала аудита", "SELECT * FROM AuditLog ORDER BY Timestamp DESC LIMIT 5"),
            ("9. Выбрать значение настройки 'DefaultCurrency'", "SELECT SettingValue FROM SystemSettings WHERE SettingName = 'DefaultCurrency'"),
            ("10. Выбрать документы, связанные со страховым случаем ID = 1", "SELECT * FROM ClaimDocuments WHERE ClaimID = 1"),
            ("11. Выбрать клиентов и их полисы (JOIN)", """
                SELECT c.FullName, p.PolicyNumber
                FROM Clients c
                JOIN Policies p ON c.ClientID = p.ClientID
            """),
            ("12. Cредняя сумма страховых выплат", "SELECT AVG(ClaimAmount) FROM Claims"),
        ]

        for i, (description, query) in enumerate(queries):
            print(f"\n--- Тест {i+1}: {description} ---")
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("Нет данных")

    except sqlite3.Error as e:
        print(f"Ошибка при выполнении тестовых запросов: {e}")
    finally:
        if conn:
            conn.close()

# Вызов функций
if __name__ == "__main__":
    #Сначала создаем базу, если ее нет
    create_database()
    #Затем заполняем таблицы
    fill_tables()
    #И выполняем тестовые запросы
    test_queries()
