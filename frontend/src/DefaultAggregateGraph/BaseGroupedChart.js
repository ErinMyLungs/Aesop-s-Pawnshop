import React, {Component} from 'react';
import {
    VictoryChart,
    VictoryGroup,
    VictoryBar,
    VictoryAxis,
    VictoryLabel,
    VictoryLegend,
    VictoryTheme,
    VictoryContainer
} from 'victory';
import PoTGraph from "../IndividualPriceOverTimeGraph/PoTGraph";
import './BaseGroupedChart.css';
import ErinGraphTheme from "../ErinTheme/ErinGraphTheme";

class BaseGroupedChart extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [
                {model: 'placeholder', nonTiPrice: 0, tiPrice: 0},
            ],
            single_model: false
        }
    }

    fetchAggregateData() {
        // fetch('./api/v0.1/model')
        fetch('http://127.0.0.1:5000/api/v0.1/model')
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
            <div>
                <div
                    className={'base-grouped-chart'}
                    style={{display: 'flex'}}
                >

                    <h3>Average GPU Price in Dollars</h3>

                    <VictoryChart
                        title={"Average GPU Price in Dollars"}
                        domainPadding={{x: 10}}
                        theme={ErinGraphTheme}
                        containerComponent={
                            <VictoryContainer
                                style={{width: "80%"}}
                            />}
                    >

                        <VictoryAxis
                            dependentAxis={true}
                            label={"Average Price ($ USD)"}
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
                            name={'testing'}
                            offset={5}
                            style={{data: {width: 5}}}
                            events={[{
                                childName: ['bar-1', 'bar-2'],
                                target: "data",
                                eventHandlers: {
                                    onClick: (event, data) => {
                                        this.setState({single_model: data.datum.model});
                                    }
                                }
                            }]}
                        >

                            <VictoryBar
                                name={'bar-1'}
                                data={this.state.data}
                                x={"model"}
                                y={"tiPrice"}
                            />

                            <VictoryBar
                                name={'bar-2'}
                                data={this.state.data}
                                x={'model'}
                                y={"nonTiPrice"}
                            />

                        </VictoryGroup>
                    </VictoryChart>
                </div>

                < div
                    className={'price-over-time-chart'}>
                    {
                        this.state.single_model !== false &&
                        <PoTGraph model={this.state.single_model}/>
                    }
                </div>

            </div>
        );
    }
}

export default BaseGroupedChart;
