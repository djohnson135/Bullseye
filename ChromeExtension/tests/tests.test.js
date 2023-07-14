import renderer from 'react-test-renderer'
import { render, fireEvent, screen } from "@testing-library/react";
import React from 'react';
import '@testing-library/jest-dom'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ReactDOM from 'react-dom';
import { enableFetchMocks } from 'jest-fetch-mock'
import userEvent from '@testing-library/user-event'
import { createMemoryHistory } from 'history';
import App from '../src/App';

describe('Popup features', () => {
    test('The Text', async () => {
        const history = createMemoryHistory();
        const { getByText } = render(
            <BrowserRouter>
                <App />
            </BrowserRouter>
        );
        expect(screen.getAllByText(/bullseye/i)[0]).toBeInTheDocument();
        expect(screen.getAllByText(/for chrome/i)[0]).toBeInTheDocument();
    });
    test('The Button', async () => {
        const history = createMemoryHistory();
        const { getByText } = render(
            <BrowserRouter>
                <App />
            </BrowserRouter>
        );
        expect(screen.getAllByText(/generate path from cart/i)[0]).toBeInTheDocument();
        const button = screen.getAllByText(/generate path from cart/i)[0];
        fireEvent.click(button);
    });
    test('The Image', async () => {
        const history = createMemoryHistory();
        const { container } = render(
            <BrowserRouter>
                <App />
            </BrowserRouter>
        );
        expect(container.getElementsByClassName('bullseye').length).toBe(1);
        expect(container.getElementsByTagName('img').length).toBe(2);
    });
    test('The Generated Path Link', async () => {
        const history = createMemoryHistory();
        const { container } = render(
            <BrowserRouter>
                <App />
            </BrowserRouter>
        );
        expect(container.getElementsByTagName('a').length).toBe(1);
    });
    test('The User', async () => {
        const history = createMemoryHistory();
        const { container } = render(
            <BrowserRouter>
                <App />
            </BrowserRouter>
        );
        expect(screen.getAllByText(/jane doe/i)[0]).toBeInTheDocument();
        expect(container.getElementsByClassName(' sb-avatar').length).toBe(1);
        expect(container.getElementsByClassName(' sb-avatar__text').length).toBe(1);
    });
});
