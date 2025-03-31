-- Tive algumas incompatibilidades com o csv, principalmente no quesito numerico
-- alterei as colunas de saldo mudando as virgulas , por pontos .

-- Tabela de Despesas
CREATE TABLE despesas_2024_T4 (
    data TEXT,  
    rege_ans TEXT,  
    cd_conta_contabil TEXT,  
    descricao TEXT,  
    vl_saldo_inicial DECIMAL(15, 2),  
    vl_saldo_final DECIMAL(15, 2)  
);

CREATE TABLE operadoras (
    registro_ans TEXT,  
    cnpj TEXT,  
    razao_social TEXT,  
    nome_fantasia TEXT,  
    modalidade TEXT,  
    logradouro TEXT,  
    numero TEXT,  
    complemento TEXT,  
    bairro TEXT,  
    cidade TEXT,  
    uf TEXT,  
    cep TEXT,  
    ddd TEXT,  
    telefone TEXT,  
    fax TEXT,  
    endereco_eletronico TEXT,  
    representante TEXT,  
    cargo_representante TEXT,  
    regiao_de_comercializacao TEXT,  
    data_registro_ans TEXT  
);


-- Importação do arquivo CSV
\copy despesas_2024_T4 FROM '/home/saberhausem/sqlteste/4T2024_formatado.csv' DELIMITER ';' CSV HEADER;
\copy operadoras FROM '/home/saberhausem/sqlteste/Relatorio_cadop.csv' DELIMITER ';' CSV HEADER;

-- 3.5 
-- considerando o ultimo semestre de 2024, arquivo: 4T2024_formatado.csv

SELECT 
    o.razao_social AS operadora,
    SUM(d.vl_saldo_final - d.vl_saldo_inicial) AS total_despesa
FROM operadoras o
JOIN despesas_2024_T4 d ON o.registro_ans = d.rege_ans
WHERE d.DESCRICAO = 'EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA À SAÚDE'
GROUP BY o.razao_social
ORDER BY total_despesa DESC
LIMIT 10;

-- 3.6 
-- considerando agora todo os trimestres de 2024

ALTER TABLE despesas_2024_T4 RENAME TO despesas_2024;

\copy despesas_2024 FROM '/home/saberhausem/sqlteste/1T2024_formatado.csv' DELIMITER ';' CSV HEADER;
\copy despesas_2024 FROM '/home/saberhausem/sqlteste/2T2024_formatado.csv' DELIMITER ';' CSV HEADER;
\copy despesas_2024 FROM '/home/saberhausem/sqlteste/3T2024_formatado.csv' DELIMITER ';' CSV HEADER;

SELECT 
    o.razao_social AS operadora,
    SUM(d.vl_saldo_final - d.vl_saldo_inicial) AS total_despesa
FROM operadoras o
JOIN despesas_2024 d ON o.registro_ans = d.rege_ans
WHERE d.DESCRICAO = 'EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA À SAÚDE'
GROUP BY o.razao_social
ORDER BY total_despesa DESC
LIMIT 10;