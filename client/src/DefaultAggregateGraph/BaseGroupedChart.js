import React from 'react';
import {VictoryChart, VictoryGroup, VictoryBar} from 'victory';

function BaseGroupedChart() {
    return (
        <div className={'base-grouped-chart'}>
            <VictoryChart>
                <VictoryGroup>
                    <VictoryBar/>
                </VictoryGroup>
            </VictoryChart>
        </div>
    )
        ;
}

export default BaseGroupedChart;