-- Гіпотеза 1: клієнти з одним продуктом швидше покидають банк,
-- бо не мають сильної прив'язаності.

SELECT NumOfProducts, Exited, COUNT(*) AS customers
FROM Bank
GROUP BY NumOfProducts, Exited
ORDER BY NumOfProducts;

-- Результат:
-- NumOfProducts | Exited | customers
-- 1             | 0      | 3675
-- 1             | 1      | 1409
-- 2             | 0      | 4242
-- 2             | 1      | 348
-- 3             | 0      | 46
-- 3             | 1      | 220
-- 4             | 1      | 60
