import React from 'react';
import {shallow} from 'enzyme';
import BaseGroupedChart from './BaseGroupedChart';

describe('Always visible graph module with aggregate GPU data', () => {
    let wrapper;
    beforeEach(() => wrapper = shallow(<BaseGroupedChart/>));

    it('should render a single <div/>', () => {
        expect(wrapper.find('div').length).toEqual(1);
    });

    it('should render a single VictoryChart component', () => {
        expect(wrapper.find('VictoryChart').length).toEqual(1);
    });

    it('should contain VictoryGroup and VictoryBar elements', () => {
        let victoryChartShallow = wrapper.find('VictoryChart').shallow();

        expect(victoryChartShallow.find('VictoryGroup').length).toEqual(1);
        expect(victoryChartShallow.find('VictoryBar').length).toEqual(1);
    });
});