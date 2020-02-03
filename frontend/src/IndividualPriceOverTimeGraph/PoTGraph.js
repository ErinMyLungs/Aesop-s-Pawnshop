import React, {Component} from 'react';
import {
    VictoryAxis,
    VictoryChart,
    VictoryGroup,
    VictoryLabel,
    VictoryLegend,
    VictoryLine,
    VictoryScatter
} from 'victory';
import './PoTGraph.css';

class PoTGraph extends Component {
    constructor(props) {
        super(props);
        this.state = {}
    }

    render() {
        return (
            <div
                className={'price-over-time-chart'}
                style={{display: 'flex'}}
            >
                <h4>Price of {this.props.model} over time</h4>

                <VictoryChart>
                    <VictoryGroup>
                        <VictoryLine/>
                        <VictoryLine/>
                        <VictoryScatter/>
                        <VictoryScatter/>
                    </VictoryGroup>
                </VictoryChart>

            </div>
        );
    }
}

export default PoTGraph;