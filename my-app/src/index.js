import React from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import './index.css';

  class LoginForm extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        id: "",
        name: "",
        type: "",
        category: "",
        quantityInStock: "",
        value: "",
        promotionalValue: "",
        availableToSell: false,
        inPromotion: false,
        insertionDate: "",
        updateDate: "",
        promotionEndDate: "",
        manufacturer: "",
        clientId: "",
        weight: "",
        description: ""
      };
  
      this.handleId = this.handleId.bind(this);
      this.handleName = this.handleName.bind(this);
      this.handleType = this.handleType.bind(this);
      this.handleCategory = this.handleCategory.bind(this);
      this.handleQuantityInStock = this.handleQuantityInStock.bind(this);
      this.handleValue = this.handleValue.bind(this);
      this.handlePromotionalValue = this.handlePromotionalValue.bind(this);
      this.handleAvailableToSell = this.handleAvailableToSell.bind(this);
      this.handleInPromotion = this.handleInPromotion.bind(this);
      this.handleInsertionDate = this.handleInsertionDate.bind(this);
      this.handleUpdateDate = this.handleUpdateDate.bind(this);
      this.handlePromotionEndDate = this.handlePromotionEndDate.bind(this);
      this.handleManufacturer = this.handleManufacturer.bind(this);
      this.handleClientId = this.handleClientId.bind(this);
      this.handleWeight = this.handleWeight.bind(this);
      this.handleDescription = this.handleDescription.bind(this);

      this.handleSubmit = this.handleSubmit.bind(this);
    }
  
    handleId(event) {
      this.setState({id: event.target.value});
    }

    handleName(event) {
      this.setState({name: event.target.value});
    }

    handleType(event) {
      this.setState({type: event.target.value});
    }

    handleCategory(event) {
      this.setState({category: event.target.value});
    }

    handleQuantityInStock(event) {
      this.setState({quantityInStock: event.target.value});
    }

    handleValue(event) {
      this.setState({value: event.target.value});
    }

    handlePromotionalValue(event) {
      this.setState({promotionalValue: event.target.value});
    }

    handleAvailableToSell(event) {
      this.setState({availableToSell: event.target.checked});
    }

    handleInPromotion(event) {
      this.setState({inPromotion: event.target.checked});
    }

    handleInsertionDate(event) {
      this.setState({insertionDate: event.target.value});
    }

    handleUpdateDate(event) {
      this.setState({updateDate: event.target.value});
    }

    handlePromotionEndDate(event) {
      this.setState({promotionEndDate: event.target.value});
    }

    handleManufacturer(event) {
      this.setState({manufacturer: event.target.value});
    }

    handleClientId(event) {
      this.setState({clientId: event.target.value});
    }

    handleWeight(event) {
      this.setState({weight: event.target.value});
    }

    handleDescription(event) {
      this.setState({description: event.target.value});
    }
  
    handleSubmit(event) {
      // alert('Things were submitted!\n'
      //       + 'id: ' +  this.state.id + '\n'
      //       + 'name: ' +  this.state.name + '\n'
      //       + 'type: ' +  this.state.type + '\n'
      //       + 'category: ' +  this.state.category + '\n'
      //       + 'quantityInStock: ' +  this.state.quantityInStock + '\n'
      //       + 'value: ' +  this.state.value + '\n'
      //       + 'promotionalValue: ' +  this.state.promotionalValue + '\n'
      //       + 'availableToSell: ' +  this.state.availableToSell + '\n'
      //       + 'inPromotion: ' +  this.state.inPromotion + '\n'
      //       + 'insertionDate: ' +  this.state.insertionDate + '\n'
      //       + 'updateDate: ' +  this.state.updateDate + '\n'
      //       + 'promotionEndDate: ' +  this.state.promotionEndDate + '\n'
      //       + 'manufacturer: ' +  this.state.manufacturer + '\n'
      //       + 'clientId: ' +  this.state.clientId + '\n'
      //       + 'weight: ' +  this.state.weight + '\n'
      //       + 'description: ' +  this.state.description + '\n'
      //       );
      // event.preventDefault();
      const product = {
        id: 1234567890,
        name: "BRM58AK",
        type: "Geladeira",
        category: "ELETRODOMESTICO",
        quantityInStock: 10,
        value: 3499.99,
        promotionalValue: 2999.99,
        availableToSell: true,
        inPromotion: false,
        insertionDate: {},
        updateDate: {},
        promotionEndDate: {},
        manufacturer: "Brastemp",
        clientId: "CRED",
        weight: 82,
        description: "Geladeira Brastemp Frost Free Duplex 500 litros cor Inox com Turbo Control"
      }
      axios.post(
        'http://ec2-18-218-218-216.us-east-2.compute.amazonaws.com:8080/api',
        {product}
      ).then(res => {
        console.log(res);
        console.log(res.data);
      });
    }
  
    render() {
      return (
        <form onSubmit={this.handleSubmit}>
          <label>
            id: <br />
            <input 
              type="number" 
              value={this.state.id} 
              onChange={this.handleId} 
            />
          </label> <br />
          <label>
            Name: <br />
            <input 
              type="text" 
              value={this.state.name} 
              onChange={this.handleName} 
            />
          </label> <br />
          <label>
            Type: <br />
            <input 
              type="text" 
              value={this.state.type} 
              onChange={this.handleType} 
            />
          </label> <br />
          <label>
            Category: <br />
            <input 
              type="text" 
              value={this.state.category} 
              onChange={this.handleCategory}
            />
          </label> <br />
          <label>
            Quantity in stock: <br />
            <input 
              type="number" 
              value={this.state.quantityInStock} 
              onChange={this.handleQuantityInStock} 
            />
          </label> <br />
          <label>
            Value: <br />
            <input 
              type="number" 
              value={this.state.value} 
              onChange={this.handleValue} 
            />
          </label> <br />
          <label>
            Promotional value: <br />
            <input 
              type="number" 
              value={this.state.promotionalValue} 
              onChange={this.handlePromotionalValue} 
            />
          </label> <br />
          <label>
            Available to sell:
            <input 
              type="checkbox" 
              checked={this.state.availableToSell}
              onChange={this.handleAvailableToSell} 
            />
          </label> <br />
          <label>
            In promotion:
            <input 
              type="checkbox" 
              checked={this.state.inPromotion}
              onChange={this.handleInPromotion} 
            />
          </label> <br />
          <label>
            Insertion date: <br />
            <input 
              type="text" 
              value={this.state.insertionDate} 
              onChange={this.handleInsertionDate} 
            />
          </label> <br />
          <label>
            Update date: <br />
            <input 
              type="text" 
              value={this.state.updateDate} 
              onChange={this.handleUpdateDate} 
            />
          </label> <br />
          <label>
            Promotion end date: <br />
            <input 
              type="text" 
              value={this.state.promotionEndDate} 
              onChange={this.handlePromotionEndDate} 
            />
          </label> <br />
          <label>
            Manufacturer: <br />
            <input 
              type="text" 
              value={this.state.manufacturer} 
              onChange={this.handleManufacturer} 
            />
          </label> <br />
          <label>
            Client ID: <br />
            <input 
              type="text" 
              value={this.state.clientId} 
              onChange={this.handleClientId} 
            />
          </label> <br />
          <label>
            Weight: <br />
            <input 
              type="number" 
              value={this.state.weight} 
              onChange={this.handleWeight} 
            />
          </label> <br />
          <label>
            Description: <br />
            <input  
              type="text" 
              value={this.state.description} 
              onChange={this.handleDescription} 
            />
          </label> <br />
          <input type="submit" value="Submit" />
        </form>
      );
    }
  }
  
  // ========================================
  
  ReactDOM.render(
    <LoginForm />,
    document.getElementById('root')
  );
  