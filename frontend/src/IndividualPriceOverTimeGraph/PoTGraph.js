import React, {Component} from 'react';
import {
    VictoryAxis,
    VictoryChart,
    VictoryGroup,
    VictoryContainer,
    VictoryLabel,
    VictoryLegend,
    VictoryLine,
    VictoryScatter
} from 'victory';
import ErinGraphTheme, {blue, colors, orange} from "../ErinTheme/ErinGraphTheme";
import './PoTGraph.css';

class PoTGraph extends Component {
    constructor(props) {
        super(props);
        this.state =
            {
                modelNumber: false,
                nonTiData: [{"post_id": "0", "datestring": "0", "created": 1515150, "price": 0}, {
                    "post_id": "1",
                    "datestring": "0",
                    "created": 1515000,
                    "price": 10
                }],
                tiData: [{"post_id": "placeholder", "datestring": "0", "created": 1515000, "price": 10}],
                placeHolder: [{"post_id": "placeholder", "datestring": "0", "created": 1515000, "price": 10}]
            }
    }

    fetchModelData(modelNumber, development) {
        if (this.state.modelNumber === modelNumber) {
        } else {

            // If development is true, route API calls to local flask server run on app.py
            const apiString = (development ?
                `http://127.0.0.1:5000/api/v0.1/model/${modelNumber}` :
                `./api/v0.1/model/${modelNumber}`);

            fetch(apiString)
                .then(results => {
                        // console.log(results.json());
                        return results.json();
                    }
                ).then(
                jsonified_data => {
                    let nonTiData = jsonified_data[0];
                    let tiData = jsonified_data[1].length === 0 ? this.state.placeHolder : jsonified_data[1];
                    const state = {
                        modelNumber: modelNumber,
                        nonTiData: nonTiData,
                        tiData: tiData
                    };
                    this.setState(state);
                }
            )
        }
    }

    convert_epoch_to_timestring(unixtime) {
        let options = {year: "2-digit", month: 'numeric', day: 'numeric'};
        let new_date_object = new Date(unixtime * 1000);
        return new_date_object.toLocaleDateString(undefined, options)
    }

    render() {
        if (this.props.model === false) {
        } else {
            this.fetchModelData(this.props.model, this.props.development);

            const axisStyle = {
                axisLabel: {fontSize: 10, padding: 30},
                tickLabels: {fontSize: 7, padding: 5}
            };

            let legendData = [
                {name: "Non-TI", symbol: {fill: blue, size: 2}},
            ];
            if (this.state.tiData[0].post_id !== 'placeholder') {
                legendData.push({name: "TI", symbol: {fill: orange, size: 2}})
            }

            return (
                <div
                    className={'price-over-time-chart'}
                    style={{display: 'flex'}}
                >

                    <h2>Price of {this.props.model} over time</h2>

                    <VictoryChart
                        theme={ErinGraphTheme}
                        containerComponent={
                            <VictoryContainer
                                style={{width: "80%"}}
                            />}
                    >

                        <VictoryAxis
                            dependentAxis
                            style={axisStyle}
                            label={"Price ($ USD)"}
                            tickFormat={(price) => `$${price}`}
                        />

                        <VictoryAxis
                            tickFormat={(unixtime) => `${this.convert_epoch_to_timestring(unixtime)}`}
                            style={axisStyle}
                            label={"Date"}
                        />

                        <VictoryGroup>

                            <VictoryLine
                                name={'non-ti-line'}
                                data={this.state.nonTiData}
                                x={'created'}
                                y={'price'}
                                style={{
                                    data: {stroke: colors[0]}
                                }}
                            />

                            <VictoryScatter
                                name={'non-ti-points'}
                                data={this.state.nonTiData}
                                x={'created'}
                                y={'price'}
                                size={1.3}
                                style={{data: {fill: colors[0]}}}
                            />

                            {/*TODO: Refactor this lower logic, it violates DRY. Maybe component?*/}
                            {
                                this.state.tiData.length !== 1 &&
                                <VictoryLine
                                    name={'ti-line'}
                                    data={this.state.tiData}
                                    x={'created'}
                                    y={'price'}
                                    style={{
                                        data: {stroke: colors[1]}
                                    }}
                                />
                            }

                            {
                                this.state.tiData[0].post_id !== 'placeholder' &&
                                <VictoryScatter
                                    name={'ti-points'}
                                    data={this.state.tiData}
                                    x={'created'}
                                    y={'price'}
                                    size={1.3}
                                    style={{
                                        data: {fill: colors[1]}
                                    }}
                                />
                            }

                        </VictoryGroup>

                        <VictoryLegend
                            x={300}
                            y={15}
                            title={"Legend"}
                            symbolSpacer={25}
                            centerTitle={false}
                            orientation="vertical"
                            rowGutter={{bottom: -10}}
                            titleComponent={<VictoryLabel dx={12} style={{fontSize: 12}}/>}
                            labelComponent={<VictoryLabel dx={-20} style={{fontSize: 8}}/>}
                            data={legendData}
                        />

                    </VictoryChart>
                </div>
            );
        }
    }
}

export default PoTGraph;