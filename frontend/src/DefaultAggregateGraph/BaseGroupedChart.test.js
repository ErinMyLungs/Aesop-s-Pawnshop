import React from 'react';
import {shallow, mount} from 'enzyme';
import BaseGroupedChart from './BaseGroupedChart';

describe('Always visible graph module with aggregate GPU data', () => {
    let wrapper;
    beforeEach(() => wrapper = shallow(<BaseGroupedChart/>));


    it('should render 3 div tags', () => {
        expect(wrapper.find('div').length).toEqual(3);
    });


    it('should render a single VictoryChart component', () => {
        expect(wrapper.find('VictoryChart').length).toEqual(1);
    });


    it('should contain VictoryGroup and two VictoryBar elements', () => {
        let victoryChartShallow = wrapper.find('VictoryChart').shallow();

        expect(victoryChartShallow.find('VictoryGroup').length).toEqual(1);
        expect(victoryChartShallow.find('VictoryBar').length).toEqual(2);
    });


    it('should render PoTGraph component only after single_model state is updated', () => {
        let mountedBaseGroupedChart = mount(<BaseGroupedChart/>);

        expect(mountedBaseGroupedChart.find('PoTGraph').length).toEqual(0);

        mountedBaseGroupedChart.setState({single_model: '1050'});
        expect(mountedBaseGroupedChart.find('PoTGraph').length).toEqual(1);
    });


});