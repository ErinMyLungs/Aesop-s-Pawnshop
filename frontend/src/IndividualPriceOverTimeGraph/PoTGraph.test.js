import React from 'react';
import {shallow} from 'enzyme';
import PoTGraph from './PoTGraph';

describe('Price over Time Module tests', () => {

    let wrapper;
    beforeEach(() => wrapper = shallow(<PoTGraph/>));

    it('should render a single div tag', () => {
        expect(wrapper.find('div').length).toEqual(1);
    });

    it('should render a VictoryChart component', () => {
        expect(wrapper.find('VictoryChart').length).toEqual(1);
    });

    it('should contain VictoryGroup, two Victoryline elements and two VictoryScatter', () =>{
        let victoryChartShallow = wrapper.find('VictoryChart').shallow();

        expect(victoryChartShallow.find('VictoryGroup').length).toEqual(1);
        expect(victoryChartShallow.find('VictoryLine').length).toEqual(2);
        expect(victoryChartShallow.find('VictoryScatter').length).toEqual(2);
    });

    it('should update title with model props submitted to it', () => {
       wrapper.setProps({model: 'foobar'});
       expect(wrapper.find('h4').text()).toEqual('Price of foobar over time')
    });

});