USE restaurante_501;

ALTER TABLE Detalle_Orden 
ADD termino VARCHAR(20) NOT NULL DEFAULT '',
    alergias NVARCHAR(MAX) NOT NULL DEFAULT '',
    notas NVARCHAR(MAX) NOT NULL DEFAULT '';

	USE restaurante_501;
SELECT TABLE_NAME, COLUMN_NAME 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME IN ('Detalle_Orden', 'OrdenRestaurante', 'Mesa', 'Factura', 'Plato')
ORDER BY TABLE_NAME, ORDINAL_POSITION;

USE restaurante_501;

DECLARE @i INT = 1;
WHILE @i <= 30
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Mesa WHERE numero_mesa = @i)
        INSERT INTO Mesa (numero_mesa, capacidad, estado_mesa) VALUES (@i, 4, 'disponible');
    SET @i = @i + 1;
END

USE restaurante_501;
ALTER TABLE OrdenRestaurante ALTER COLUMN empleado_id BIGINT NULL;
