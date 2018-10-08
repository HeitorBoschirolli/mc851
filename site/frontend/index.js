import React from 'react';
import ReactDOM from 'react-dom';
// import axios from 'axios';
import './index.css';
import $ from 'jquery';

  class Teste extends React.Component {

    constructor(props) {
      super(props);
      this.state = {
        email: '',
        senha: '',
        cpf: '',
        nome: '',
        dataDeNascimento: '',
        telefone: '',
        idGrupo: '',
      }

      this.handleEmail = this.handleEmail.bind(this);
      this.handleSenha = this.handleSenha.bind(this);
      this.handleCPF = this.handleCPF.bind(this);
      this.handleNome = this.handleNome.bind(this);
      this.handleDataNascimento = this.handleDataNascimento.bind(this);
      this.handleTelefone = this.handleTelefone.bind(this);
      this.handleIdGrupo = this.handleIdGrupo.bind(this);
      this.realizaPOST = this.realizaPOST.bind(this);
    }

    realizaPOST(event) {

      $.ajax({
          type:"POST",
          url:"http://127.0.0.1:8080/backend/teste",
          contentType: 'application/json; charset=UTF-8',
          data: JSON.stringify(
            {
              "email": this.state.email,
            	"senha": this.state.senha,
            	"cpf": this.state.cpf,
            	"nome": this.state.nome,
            	"dataDeNascimento": this.state.dataDeNascimento,
            	"telefone": this.state.telefone,
            	"idGrupo": this.state.idGrupo
            }

          ),
          success: res => {
              alert(res.registerToken);
          },
          error: function(xhr, status, err) {
            alert('ERRO1: ' + xhr.status);
            console.error(xhr, status, err.toString());
        }
      });

      event.preventDefault();

    }

    handleEmail(event) {
      this.setState({email: event.target.value});
    }

    handleSenha(event) {
      this.setState({senha: event.target.value});
    }

    handleCPF(event) {
      this.setState({cpf: event.target.value});
    }

    handleNome(event) {
      this.setState({nome: event.target.value});
    }

    handleDataNascimento(event) {
      this.setState({dataDeNascimento: event.target.value});
    }

    handleTelefone(event) {
      this.setState({telefone: event.target.value});
    }

    handleIdGrupo(event) {
      this.setState({idGrupo: event.target.value});
    }

    render() {

      const divStyle = {
        color: 'black',
        height: '25px',
        textAlign: 'center',
      };

      const buttonStyle = {
        height: '50px',
        textAlign: 'center'
      }

      return (
          <form onSubmit={this.realizaPOST}>

            <div style={divStyle}>Email:</div>
            <div style={divStyle}>
              <input type="text" value={this.state.email} onChange={this.handleEmail} />
            </div>


            <div style={divStyle}>Senha:</div>
            <div style={divStyle}>
              <input type="text" value={this.state.senha} onChange={this.handleSenha} />
            </div>

            <div style={divStyle}>Cpf:</div>
            <div style={divStyle}>
                <input type="text" value={this.state.cpf} onChange={this.handleCPF} />
            </div>

            <div style={divStyle}>Nome:</div>
            <div style={divStyle}>
                <input type="text" value={this.state.nome} onChange={this.handleNome} />
            </div>


            <div style={divStyle}>Data de Nascimento:</div>
            <div style={divStyle}>
                <input type="text" value={this.state.dataDeNascimento} onChange={this.handleDataNascimento} />
            </div>

            <div style={divStyle}>Telefone:</div>
            <div style={divStyle}>
                <input type="text" value={this.state.telefone} onChange={this.handleTelefone} />
            </div>

            <div style={divStyle}>idGrupo:</div>
            <div style={divStyle}>
                <input type="text" value={this.state.idGrupo} onChange={this.handleIdGrupo} />
            </div>

            <div style={buttonStyle}>
              <input type="submit" value="ENVIA REQUISIÇÃO" />
            </div>
        </form>

      );
    }
  }


  // ========================================

  ReactDOM.render(
    <Teste />,
    document.getElementById('root')
  );
