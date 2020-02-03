import React, {Component} from 'react';
import {VictoryChart, VictoryGroup, VictoryBar, VictoryAxis, VictoryLabel, VictoryLegend} from 'victory';
import './BaseGroupedChart.css';

class BaseGroupedChart extends Component {
    constructor(props) {
        super(props);
        this.state = {
            //Placeholder data TODO: Hook into flask api

            data: [
                {model: ' ', nonTiPrice: 0, tiPrice: 0},

            ],

        }
    }

fetchAggregateData() {
        fetch('./api/v0.1/model')
            .then(results => {
                return results.json();
                }
            ).then(
                jsonified_data => {
                    this.setState({data: jsonified_data});
                }
        )
}

    render() {

        if (this.state.data.length === 1) {
            this.fetchAggregateData()
        }

        return (
            <div
                className={'base-grouped-chart'}
                style={{display: 'flex'}}
            >

                <h3>Average GPU Price in Dollars</h3>

                <VictoryChart
                    title={"Average GPU Price in Dollars"}
                    domainPadding={{x: 10}}
                >
                    {/*TODO: Add legend*/}
                    <VictoryAxis
                        dependentAxis={true}
                        label={"Average Price ($USD"}
                        tickFormat={(Price) => `$${Price}`}
                        style={{
                            axisLabel: {fontSize: 10, padding: 30},
                            tickLabels: {fontSize: 7, padding: 5}
                        }}
                    />

                    <VictoryAxis
                        dependentAxis={false}
                        label={"GPU Models (Arranged by Generation)"}
                        tickLabelComponent={<VictoryLabel dy={-3}/>}
                        style={{
                            axisLabel: {fontSize: 10, padding: 30, angle: 0},
                            tickLabels: {fontSize: 7, padding: 20, angle: -45}
                        }}
                    />

                    <VictoryGroup
                        offset={5}
                        colorScale={'qualitative'}
                        style={{data: {width: 5}}}
                    >

                        <VictoryBar
                            data={this.state.data}
                            x={"model"}
                            y={"tiPrice"}
                        />

                        <VictoryBar
                            data={this.state.data}
                            x={'model'}
                            y={"nonTiPrice"}
                        />

                    </VictoryGroup>
                </VictoryChart>
            </div>

        );
    }
}

export default BaseGroupedChart;