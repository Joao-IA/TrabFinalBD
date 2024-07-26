SELECT 
    DISTINCT 
    (julianday(e.DataHoraInicio) - 2440587.5) AS DataID,
    DATE(e.DataHoraInicio) AS Data, 
    strftime('%W', e.DataHoraInicio) AS Semana, 
    strftime('%m', e.DataHoraInicio) AS Mes, 
    strftime('%Y', e.DataHoraInicio) AS Ano
FROM 
    Entregas e;
