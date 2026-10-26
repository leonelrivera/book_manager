-- ============================================================================
-- Tabla: auditoria
-- Registra la traza cronológica de operaciones ejecutadas en el sistema.
-- Campos requeridos (Sprint 3 - Ejercicio 06):
--   - accion: Acción ejecutada
--   - fecha: Timestamp de ejecución
--   - detalles: Parámetros y resultado de la operación
-- ============================================================================

CREATE TABLE IF NOT EXISTS auditoria (
    id SERIAL PRIMARY KEY,
    accion VARCHAR(100) NOT NULL,
    fecha TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    detalles TEXT
);

CREATE INDEX IF NOT EXISTS idx_auditoria_fecha ON auditoria(fecha DESC);
CREATE INDEX IF NOT EXISTS idx_auditoria_accion ON auditoria(accion);
