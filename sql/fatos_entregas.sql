SELECT 
    e.EntregaID, 
    e.DataHoraInicio, 
    e.DataHoraFim, 
    (julianday(e.DataHoraFim) - julianday(e.DataHoraInicio)) * 24 AS TempoEntrega,
    c.ClienteID, 
    p.ProdutoID, 
    v.VeiculoID, 
    m.MotoristaID
FROM 
    Entregas e
JOIN 
    Pedidos d ON e.PedidoID = d.PedidoID
JOIN 
    Clientes c ON d.ClienteID = c.ClienteID
JOIN 
    Produtos p ON d.ProdutoID = p.ProdutoID
JOIN 
    Veiculos v ON e.VeiculoID = v.VeiculoID
JOIN 
    Motoristas m ON v.VeiculoID = m.VeiculoID;
