-- Створення таблиці Bank та завантаження підготовлених даних
-- (дані підготовлені у Google Sheets, див. 01-data-preparation/data_preparation.md)

CREATE TABLE Bank (
    CustomerId       INT PRIMARY KEY,
    Surname          VARCHAR(50),
    CreditScore      INT,
    Geography        VARCHAR(20),
    Gender           VARCHAR(6),
    Age              INT,
    Tenure           INT,
    Balance          DECIMAL(10,2),
    NumOfProducts    INT,
    HasCrCard        BOOLEAN,
    IsActiveMember   BOOLEAN,
    EstimatedSalary  DECIMAL(10,2),
    Exited           BOOLEAN
);

-- Дані завантажені через згенеровані INSERT INTO (10 000 рядків),
-- приклад одного з батчів:
INSERT INTO Bank (CustomerId, Surname, CreditScore, Geography, Gender, Age, Tenure,
                   Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, Exited)
VALUES
    (15634602, 'Hargrave', 619, 'France', 'Female', 42, 2, 0,       1, 1, 1, 101348.88, 1),
    (15647311, 'Hill',     608, 'Spain',  'Female', 41, 1, 83807.86, 1, 0, 1, 112542.58, 0),
    (15619304, 'Onio',     502, 'France', 'Female', 42, 8, 159660.80, 3, 1, 0, 113931.57, 1),
    (15701354, 'Boni',     699, 'France', 'Female', 39, 1, 0,       2, 0, 0, 93826.63,  0),
    (15737888, 'Mitchell', 850, 'Spain',  'Female', 43, 2, 125510.82, 1, 1, 1, 79084.10,  0),
    (15574012, 'Chu',      645, 'Spain',  'Male',   44, 8, 113755.78, 2, 1, 0, 149756.71, 1),
    (15592531, 'Bartlett', 822, 'France', 'Male',   50, 7, 0,       2, 1, 1, 10062.80,  0);
-- ... (усього 10 000 рядків; повний скрипт INSERT згенеровано у Google Sheets)
