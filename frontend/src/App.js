import React from 'react';
import './App.css';
import BaseGroupedChart from "./DefaultAggregateGraph/BaseGroupedChart";
import PoTGraph from "./IndividualPriceOverTimeGraph/PoTGraph";

function App() {
    return (
        <div className="App">
            <h1>Used GPU Market on /r/hardwareswap</h1>
            <p> A visualization dashboard to look at used GPU pricing for NVidia GPUs. </p>
            <BaseGroupedChart/>
        </div>
    );
}

export default App;
