import React from "react";
import Menu from './Menu';
import "./App.scss";

function App() {

    const items = [
        { key: 1, value: 'a'},
        { key: 2, value: 'b'}
    ];

    return (
        <div className="App">
           <Menu items={items} />
        </div>
    );
}

export default App;
