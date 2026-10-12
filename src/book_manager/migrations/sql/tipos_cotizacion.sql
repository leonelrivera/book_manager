-- Migración de datos para la tabla: tipos_cotizacion
-- Total de registros: 10

INSERT INTO tipos_cotizacion (id, nombre, descripcion) VALUES (1, 'Oficial', 'Cotizacion oficial del Banco Central');
INSERT INTO tipos_cotizacion (id, nombre, descripcion) VALUES (2, 'Blue', 'Cotizacion informal del mercado libre');
INSERT INTO tipos_cotizacion (id, nombre, descripcion) VALUES (3, 'MEP', 'Dolar Mercado Electronico de Pagos (Bolsa)');
INSERT INTO tipos_cotizacion (id, nombre, descripcion) VALUES (4, 'CCL', 'Contado con Liquidacion');
INSERT INTO tipos_cotizacion (id, nombre, descripcion) VALUES (5, 'Tarjeta', 'Dolar aplicable a consumos con tarjeta en el exterior');
INSERT INTO tipos_cotizacion (id, nombre, descripcion) VALUES (6, 'Mayorista', 'Dolar para operaciones comerciales mayoristas');
INSERT INTO tipos_cotizacion (id, nombre, descripcion) VALUES (7, 'Cripto', 'Cotizacion basada en monedas estables (USDT/USDC)');
INSERT INTO tipos_cotizacion (id, nombre, descripcion) VALUES (8, 'Solidario', 'Dolar con recargo impositivo');
INSERT INTO tipos_cotizacion (id, nombre, descripcion) VALUES (9, 'Ahorro', 'Dolar para atesoramiento de personas fisicas');
INSERT INTO tipos_cotizacion (id, nombre, descripcion) VALUES (10, 'Futuro', 'Cotizacion en mercados a termino Rofex');
