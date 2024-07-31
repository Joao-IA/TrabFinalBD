SELECT 
    (julianday(e.DataHoraInicio) - 2440587.5) AS DataID,
    e.EntregaID, 
    e.Estado,
    e.Latitude,
    e.Longitude,
    e.StatusEntrega,
    e.DataHoraInicio, 
    e.DataHoraFim, 
    e.PedidoID,
    d.ProdutoID,
    (julianday(e.DataHoraFim) - julianday(e.DataHoraInicio)) * 24 AS TempoEntrega,
    c.ClienteID, 
    v.VeiculoID,
    m.MotoristaID
FROM 
    Entregas e
JOIN 
    Pedidos d ON e.PedidoID = d.PedidoID
JOIN 
    Clientes c ON d.ClienteID = c.ClienteID
JOIN 
    Veiculos v ON e.VeiculoID = v.VeiculoID
JOIN 
    Motoristas m ON e.MotoristaID = m.MotoristaID
JOIN
    Produtos p ON e.ProdutoID = p.ProdutoID
