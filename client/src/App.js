import React from 'react';
import {VictoryBar} from 'victory';
import './App.css';

function App() {
    return (
        <div className="App">
            <h1>Used GPU Market on /r/hardwareswap</h1>
            <p> A visualization dashboard to look at used GPU pricing for NVidia GPUs. </p>
            <VictoryBar/>
        </div>
    );
}

export default App;
