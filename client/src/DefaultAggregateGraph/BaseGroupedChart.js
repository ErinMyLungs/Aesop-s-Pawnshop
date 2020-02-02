import React, {Component} from 'react';
import {VictoryChart, VictoryGroup, VictoryBar, VictoryAxis, VictoryLabel, VictoryLegend} from 'victory';

class BaseGroupedChart extends Component {
    constructor(props) {
        super(props);
        this.state = {
            //Placeholder data TODO: Hook into flask api
            models: ['760', '780', '950', '960', '970', '980', '1030', '1050', '1060', '1070', '1080', '1650', '1660', '2060', '2070', '2080'],
            non_ti: [69, 107, 56, 81, 102, 201, 64, 103, 154, 240, 347, 132, 168, 315, 430, 610],
            ti: [0, 110, 0, 0, 0, 235, 0, 104, 0, 285, 494, 0, 221, 0, 0, 562],
        }
    }

    render() {
        // let ticks = Array.from(this.state.models.keys(), x => x+1); TODO: Possibly use to refactor for consistent label placement?
        return (
            <div
                className={'base-grouped-chart'}
                style={{display: 'flex'}}
            >
                <VictoryChart
                    domainPadding={{x: 10}}
                >
                    <VictoryAxis
                        dependentAxis={true}
                        label={"Average Price ($USD"}
                        style={{
                            axisLabel: {fontSize: 10, padding: 20},
                            tickLabels: {fontSize: 7, padding: 5}
                        }}
                    />

                    <VictoryAxis
                        dependentAxis={false}
                        label={"GPU Models (Arranged by Generation)"}
                        style={{
                            axisLabel: {fontSize: 10, padding: 30, angle: 0},
                            tickLabels: {fontSize: 7, padding: 10, angle: -90}
                        }}
                    />

                    <VictoryGroup
                        offset={5}
                        colorScale={'qualitative'}
                        style={{data: {width: 5}}}
                    >

                        <VictoryBar
                            data={this.state.models.map((e, i) => [e, this.state.non_ti[i]])}
                            x={0}
                            y={1}
                        />

                        <VictoryBar
                            data={this.state.models.map((e, i) => [e, this.state.ti[i]])}
                            x={0}
                            y={1}
                        />

                    </VictoryGroup>
                </VictoryChart>
            </div>

        );
    }
}

export default BaseGroupedChart;