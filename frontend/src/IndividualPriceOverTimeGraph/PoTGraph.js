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
import ErinGraphTheme from "../ErinTheme/ErinGraphTheme";
import './PoTGraph.css';

class PoTGraph extends Component {
    constructor(props) {
        super(props);
        this.state = {
            modelNumber: false,
            nonTiData: [
                {"post_id": "0", "datestring": "0", "created": 1515150, "price": 0},
                {"post_id": "1", "datestring": "0", "created": 1515000, "price": 10}
            ],
            tiData: [{"post_id": "placeholder", "datestring": "0", "created": 1515000, "price": 10}]
        }
    }

    fetchModelData(modelNumber) {
        if (this.state.modelNumber === modelNumber) {
        } else {
            // const apiString = `./api/v0.1/model/${modelNumber}`;
            const apiString = `http://127.0.0.1:5000/api/v0.1/model/${modelNumber}`;
            fetch(apiString)
                .then(results => {
                        return results.json();
                    }
                ).then(
                jsonified_data => {
                    let nonTiData = jsonified_data[0];
                    let tiData = jsonified_data[1];
                    let state = {
                        modelNumber: modelNumber,
                        nonTiData: nonTiData,
                        tiData: tiData.length === 0 ? [{
                            "post_id": "placeholder",
                            "datestring": "0",
                            "created": 1515000,
                            "price": 10
                        }] : tiData
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
            this.fetchModelData(this.props.model);

            const axisStyle = {
                axisLabel: {fontSize: 10, padding: 30},
                tickLabels: {fontSize: 7, padding: 5}
            };

            return (
                <div
                    className={'price-over-time-chart'}
                    style={{display: 'flex'}}
                >
                    <h4>Price of {this.props.model} over time</h4>

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
                        />

                        <VictoryGroup>

                            <VictoryLine
                                name={'non-ti-line'}
                                data={this.state.nonTiData}
                                x={'created'}
                                y={'price'}
                            />
                            <VictoryScatter
                                name={'non-ti-points'}
                                data={this.state.nonTiData}
                                x={'created'}
                                y={'price'}
                                size={1.3}
                            />
                            {/*TODO: Refactor this lower logic, it violates DRY. Maybe component?*/}
                            {
                                this.state.tiData.length !== 1 &&
                                <VictoryLine
                                    name={'ti-line'}
                                    data={this.state.tiData}
                                    x={'created'}
                                    y={'price'}
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

                                />
                            }

                        </VictoryGroup>
                    </VictoryChart>

                </div>
            );
        }
    }
}

export default PoTGraph;