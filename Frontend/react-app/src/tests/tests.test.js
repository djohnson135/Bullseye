import renderer from 'react-test-renderer'
import { render, fireEvent, screen } from "@testing-library/react";
import Head from '../components/Head'
import Footer from '../components/Footer';
import React from 'react';
import NavigationBar from '../components/NavigationBar';
import HeroSection from '../components/HeroSection';
import InfoSection from '../components/InfoSection';
import LandingSection from '../components/LandingSection';
import PathSection from '../components/PathSection';
import AisleListSection from '../components/AisleListSection';
import Home from '../components/pages/Home';
import List from '../components/pages/List';
import '@testing-library/jest-dom'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ReactDOM from 'react-dom';
import { enableFetchMocks } from 'jest-fetch-mock'
import userEvent from '@testing-library/user-event'
import { createMemoryHistory } from 'history';

// Unit testing components connectivity: 
describe('Head has necessary parts', () => {
    test('renders the title', () => {
        render(<Head />);
        const titleElement = screen.getByText(/welcome to bullseye/i);
        expect(titleElement).toBeInTheDocument();
    });
});

describe('Navbar has necessary parts', () => {
    test('renders the navbar buttons', () => {
        render(<BrowserRouter><NavigationBar /> </BrowserRouter>);
        const titleElement = screen.getByText(/home/i);
        const titleElement2 = screen.getByText(/list/i);
        const titleElement3 = screen.getByText(/path/i);
        const titleElement4 = screen.getByText(/sequence/i);
        expect(titleElement).toBeInTheDocument();
        expect(titleElement2).toBeInTheDocument();
        expect(titleElement3).toBeInTheDocument();
        expect(titleElement4).toBeInTheDocument();
    });
});

describe('Footer has necessary parts', () => {
    test('renders the footer', () => {
        render(<BrowserRouter><Footer /></BrowserRouter>);
        const titleElement = screen.getByText(/sign in for your improved shopping experience./i);
        expect(titleElement).toBeInTheDocument();
    });
});

describe('HeroSection has necessary parts', () => {
    test('renders the slides', () => {
        render(<BrowserRouter><HeroSection /></BrowserRouter>);
        const titleElement = screen.getByText(/for your improved shopping experience/i);
        expect(titleElement).toBeInTheDocument();
    });
    test('check for buttons', () => {
        const { container } = render(<BrowserRouter><HeroSection /></BrowserRouter>)
        expect(container.getElementsByClassName('bgImg-hero2').length).toBe(1);
        expect(container.getElementsByClassName('bgImg-hero').length).toBe(1);
    });
});

describe('InfoSection has necessary parts', () => {
    test('renders the descriptive text', () => {
        render(<BrowserRouter><InfoSection /></BrowserRouter>);
        const titleElement = screen.getByText(/easy/i);
        expect(titleElement).toBeInTheDocument();
        const titleElement2 = screen.getByText(/to use/i);
        expect(titleElement2).toBeInTheDocument();
        const titleElement3 = screen.getByText(/high-quality/i);
        expect(titleElement3).toBeInTheDocument();
        const titleElement4 = screen.getByText(/Groceries yourself/i);
        expect(titleElement4).toBeInTheDocument();
    });
    test('check for pictures', () => {
        const { container } = render(<BrowserRouter><InfoSection /></BrowserRouter>)
        expect(container.getElementsByClassName('flexbox-item flexbox-item3').length).toBe(1);
        expect(container.getElementsByClassName('flexbox-item flexbox-item2').length).toBe(1);
        expect(container.getElementsByClassName('flexbox-item flexbox-item1').length).toBe(1);
        expect(container.getElementsByTagName('img').length).toBe(3);
    });
});

describe('LandingSection has necessary parts', () => {
    test('renders the text', () => {
        render(<BrowserRouter><LandingSection /></BrowserRouter>);
        const titleElement = screen.getByText(/groceries made easy/i);
        expect(titleElement).toBeInTheDocument();
        const titleElement2 = screen.getByText(/learn more/i);
        expect(titleElement2).toBeInTheDocument();
    });
    test('check for video', () => {
        const { container } = render(<BrowserRouter><LandingSection /></BrowserRouter>)
        expect(container.getElementsByTagName('video').length).toBe(1);
    });
});

// Integration testing components connectivity: 
describe('Various pages go to their respective pages', () => {
    test('clicks the button to go to path section', async () => {
        // render(<BrowserRouter><HeroSection /></BrowserRouter>);
        const history = createMemoryHistory();
        const { getByText } = render(
            <BrowserRouter history={history}>
                <HeroSection />
                <PathSection />
            </BrowserRouter>
        );

        const button = screen.getAllByText('GET STARTED')[0];
        fireEvent.click(button);
        expect(history.location.pathname).toBe('/');
        expect(screen.getByText(/optimal/i)).toBeInTheDocument();
    });
    test('clicks the button to go to sequence section', async () => {
        const history = createMemoryHistory();
        const { getByText } = render(
            <BrowserRouter history={history}>
                <NavigationBar />
                <AisleListSection />
            </BrowserRouter>
        );

        const button = screen.getAllByText('Sequence')[0];
        fireEvent.click(button);
        expect(history.location.pathname).toBe('/');
        expect(screen.getByText(/sequence of your/i)).toBeInTheDocument();
    });
    test('clicks the button to go to home section', async () => {
        const history = createMemoryHistory();
        const { getByText } = render(
            <BrowserRouter history={history}>
                <NavigationBar />
                <Home />
            </BrowserRouter>
        );

        const button = screen.getAllByText('Home')[0];
        fireEvent.click(button);
        expect(history.location.pathname).toBe('/');
        expect(screen.getByText(/Bullseye helps Target shoppers efficiently/i)).toBeInTheDocument();
    });
    test('clicks the button to go to list section', async () => {
        const history = createMemoryHistory();
        const { getByText } = render(
            <BrowserRouter history={history}>
                <NavigationBar />
                <List />
            </BrowserRouter>
        );

        const button = screen.getAllByText('List')[0];
        fireEvent.click(button);
        expect(history.location.pathname).toBe('/');
        expect(screen.getByText(/improved shopping experience./i)).toBeInTheDocument();
    });
});
