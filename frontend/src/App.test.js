import React from 'react';
import {shallow} from 'enzyme';
import App from './App';

describe('App basic test', () => {
    let wrapper;
    beforeEach(() => wrapper = shallow(<App/>));

    it('should render a single <div/> tag', () => {
        expect(wrapper.find('div').length).toEqual(1);
    });

    it('should render a title with proper text', () => {
        expect(wrapper.find('h1').length).toEqual(1);
        expect(wrapper.find('h1').text()).toEqual('Used GPU Market on /r/hardwareswap');
    });

    it('should render a BaseGroupedChart component', () => {
        expect(wrapper.find('BaseGroupedChart').length).toEqual(1);
    });

});
