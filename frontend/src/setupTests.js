
import { mount } from 'enzyme';
import { act } from 'react-dom/test-utils';
import App from './App';
import Beliefs from './pages/american_beliefs';
import Carbon from './pages/carbon';
import Fight from './pages/fight_cc';
import Temperatures from './pages/global_temperatures';
import Sea from './pages/sea_level';
// import * as utils from './utils';
import { render, screen } from '@testing-library/react';


beforeEach(jest.spyOn(console, 'error').mockImplementation(() => undefined));
afterEach(() => jest.clearAllMocks());



test('renders learn react link', () => {
    render(<App />);
    const linkElement = screen.getByText(/Climavision/i);
    expect(linkElement).toBeInTheDocument();
});  

test('renders learn react link', () => {
    render(<Beliefs />);
    const linkElement = screen.getByText(/Beliefs/i);
    expect(linkElement).toBeInTheDocument();
});  


test('renders learn react link', () => {
    render(<Carbon />);
    const linkElement = screen.getByText(/Carbon/i);
    expect(linkElement).toBeInTheDocument();
});  

test('renders learn react link', () => {
    render(<Fight />);
    const linkElement = screen.getByText(/Fight/i);
    expect(linkElement).toBeInTheDocument();
});  

test('renders learn react link', () => {
    render(<Temperatures />);
    const linkElement = screen.getByText(/Temperatures/i);
    expect(linkElement).toBeInTheDocument();
});

test('renders learn react link', () => {
    render(<Sea />);
    const linkElement = screen.getByText(/Sea/i);
    expect(linkElement).toBeInTheDocument();
});






