<template>
  <div id="app">
    <h1>Pesquisa de Empresa</h1>
    <div>
      <input v-model="nome" type="text" placeholder="Digite o nome da empresa" />
      <button @click="buscarEmpresa">Buscar</button>
    </div>
    <div v-if="empresas.length">
      <h2>Resultado da Pesquisa</h2>
      <table>
        <thead>
          <tr>
            <th>Registro ANS</th>
            <th>CNPJ</th>
            <th>Razão Social</th>
            <th>Nome Fantasia</th>
            <th>Modalidade</th>
            <th>Logradouro</th>
            <th>Número</th>
            <th>Complemento</th>
            <th>Bairro</th>
            <th>Cidade</th>
            <th>UF</th>
            <th>CEP</th>
            <th>DDD</th>
            <th>Telefone</th>
            <th>Fax</th>
            <th>Email</th>
            <th>Representante</th>
            <th>Cargo Representante</th>
            <th>Região de Comercialização</th>
            <th>Data Registro ANS</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="empresa in empresas" :key="empresa.CNPJ">
            <td>{{ empresa.Registro_ANS }}</td>
            <td>{{ empresa.CNPJ }}</td>
            <td>{{ empresa.Razao_Social }}</td>
            <td>{{ empresa.Nome_Fantasia }}</td>
            <td>{{ empresa.Modalidade }}</td>
            <td>{{ empresa.Logradouro }}</td>
            <td>{{ empresa.Numero }}</td>
            <td>{{ empresa.Complemento }}</td>
            <td>{{ empresa.Bairro }}</td>
            <td>{{ empresa.Cidade }}</td>
            <td>{{ empresa.UF }}</td>
            <td>{{ empresa.CEP }}</td>
            <td>{{ empresa.DDD }}</td>
            <td>{{ empresa.Telefone }}</td>
            <td>{{ empresa.Fax }}</td>
            <td>{{ empresa.Endereco_eletronico }}</td>
            <td>{{ empresa.Representante }}</td>
            <td>{{ empresa.Cargo_Representante }}</td>
            <td>{{ empresa.Regiao_de_Comercializacao }}</td>
            <td>{{ empresa.Data_Registro_ANS }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="erro">
      <p style="color: red;">{{ erro }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      nome: '',
      empresas: [],
      erro: null
    };
  },
  methods: {
    async buscarEmpresa() {
      try {
        const response = await axios.get(`http://localhost:8000/empresa/${this.nome}`);
        this.empresas = response.data;
        this.erro = null;
      } catch (error) {
        this.erro = "Nenhuma empresa encontrada.";
        this.empresas = [];
      }
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
}
th {
  background-color: #f4f4f4;
}
</style>
