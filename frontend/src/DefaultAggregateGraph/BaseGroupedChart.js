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
        const development = true;

        if (development === false) {
            if (this.state.data.length === 1) {
                this.fetchAggregateData()
            }
        }
        else if (this.state.data.length ===1 && development === true){
            this.setState({data:[{model: '760', nonTiPrice: 69, tiPrice: 0},
                    {model: '780', nonTiPrice: 107, tiPrice: 110},
                    {model: '950', nonTiPrice: 56, tiPrice: 0},
                    {model: '960', nonTiPrice: 81, tiPrice: 0},
                    {model: '970', nonTiPrice: 102, tiPrice: 0},
                    {model: '980', nonTiPrice: 201, tiPrice: 235},
                    {model: '1030', nonTiPrice: 64, tiPrice: 0},
                    {model: '1050', nonTiPrice: 103, tiPrice: 104},
                    {model: '1060', nonTiPrice: 154, tiPrice: 0},
                    {model: '1070', nonTiPrice: 240, tiPrice: 285},
                    {model: '1080', nonTiPrice: 347, tiPrice: 494},
                    {model: '1650', nonTiPrice: 132, tiPrice: 0},
                    {model: '1660', nonTiPrice: 168, tiPrice: 221},
                    {model: '2060', nonTiPrice: 315, tiPrice: 0},
                    {model: '2070', nonTiPrice: 430, tiPrice: 0},
                    {model: '2080', nonTiPrice: 610, tiPrice: 562},]})
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