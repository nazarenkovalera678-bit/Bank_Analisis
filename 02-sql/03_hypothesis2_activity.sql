-- Гіпотеза 2: неактивні клієнти (IsActiveMember = 0) — основна група ризику відтоку.

SELECT IsActiveMember,
       COUNT(*) AS Clients,
       SUM(Exited) AS Churned,
       ROUND(AVG(Exited) * 100, 2) AS ChurnRate
FROM Bank
GROUP BY IsActiveMember
ORDER BY IsActiveMember;

-- Результат:
-- IsActiveMember | Clients | Churned | ChurnRate
-- 0              | 4849    | 1302    | 26.85
-- 1              | 5151    | 735     | 14.27
