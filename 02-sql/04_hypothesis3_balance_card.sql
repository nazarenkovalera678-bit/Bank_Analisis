-- Гіпотеза 3: клієнти з високим балансом, але без кредитки (HasCrCard = 0),
-- можуть не отримувати додаткових бонусів і йти до інших банків.

SELECT HasCrCard,
       COUNT(*) AS TotalClients,
       SUM(Exited) AS Churned,
       ROUND(AVG(Exited) * 100, 2) AS ChurnRate
FROM Bank
WHERE Balance >= 100000
GROUP BY HasCrCard;

-- Результат:
-- HasCrCard | TotalClients | Churned | ChurnRate
-- 0         | 1424         | 355     | 24.93
-- 1         | 3375         | 856     | 25.36
