import React from 'react';
import GoogleOuath from './GoogleOuath';
import { Link } from 'react-router-dom';
import './Footer.css';

function Footer() {
    return (
        <div className='footerBg' >
            <div className='footer-subscription'>
                <p className='footer-subscription-heading'>
                    Sign in for your improved shopping experience.
                </p>
                <div className='SignIn-Footer'>
                    <GoogleOuath />
                </div>
            </div>
            <div className='foooter-logo-font'>
                2023 Bullseye
            </div>
        </div>
    );
};

export default Footer;