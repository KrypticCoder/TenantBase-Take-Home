import React, { Component } from "react";
import Menu from './Menu';
import "./App.scss";

import io from 'socket.io-client';
const socket = io('http://localhost:8000');

class App extends Component {
    constructor() {
        super();
        this.state = {
            items: []
        }
    }

    componentDidMount() {
        socket.on("return_items", data => {
            const { items } = data;
            this.setState({ items });
        });
    }
    
    render() {
        const { items } = this.state;
    
        return (
            <div className="App">
                <Menu items={items} />
            </div>
        );
    }
}

export default App;