import React from 'react';
import './LandingSection.css';
import { Link } from 'react-router-dom';

function LandingSection() {
    return (
        <div>
            <video className='landingVideo' playsinline autoPlay muted loop src="video/market.mp4"></video>
            <div class="text">
                <h1><span class="chromeColor">Bullseye</span> for Target</h1>
                <p>Groceries Made Easy</p>
                <br />
                <center>
                    <Link to='/Home'>
                        <button class="learnMoreButton" href='/Home'>
                            LEARN MORE
                        </button>
                    </Link>
                </center>
                <br />
                <br />
                <br />
            </div>
        </div>
    );
};

export default LandingSection;