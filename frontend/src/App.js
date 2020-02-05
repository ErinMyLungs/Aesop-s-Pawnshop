import React from 'react';
import './App.css';
import BaseGroupedChart from "./DefaultAggregateGraph/BaseGroupedChart";

function App() {
    const development = false;
    return (
        <div className="App">
            <h1>Used GPU Market on /r/hardwareswap</h1>
            <p> A visualization dashboard to look at used GPU pricing for NVidia GPUs. </p>
            <BaseGroupedChart development={development}/>
        </div>
    );
}

export default App;
