import React from 'react';
import '../App.css';
import './InfoSection.css';

function InfoSection() {
    return (
        <div className='info-container'>
            <h0>What is <span className="info-red">Bullseye?</span></h0>
            <p0>Bullseye helps Target shoppers efficiently
                retrieve items on their shopping list. Making
                the in-store user experience at Target
                straightforward. Given a user’s shopping list
                and store, our system will find an optimal
                route for the shopper to obtain their items.</p0>

            <div className='info-container2'>
                {/* {<h1>Our Mission</h1>}
                <h2>We provide an optimal in-store route according to user's shopping list.</h2> */}
                <div className='flexbox-container'>
                    <div className='flexbox-item flexbox-item1'>
                        <img src='/img/easy-use.png' style={{ width: '40px', height: '40px', borderRadius: '5px', marginBottom: '10px' }} class="rounded mx-auto d-block" />
                        <h3>Easy</h3>
                        <h3>to use</h3>
                        <p3>Use our chrome extension or your mobile phone to get the optimal route</p3>
                    </div>
                    <div className='flexbox-item flexbox-item2'>
                        <img src='/img/route.png' style={{ width: '40px', height: '40px', borderRadius: '5px', marginBottom: '10px' }} class="rounded mx-auto d-block" />
                        <h3>Optimal</h3>
                        <h3>Route</h3>
                        <p3>According to your shopping list, you will get the shortest in-store route immediately</p3>
                    </div>
                    <div className='flexbox-item flexbox-item3'>
                        <img src='/img/grocery.png' style={{ width: '40px', height: '40px', borderRadius: '5px', marginBottom: '10px' }} class="rounded mx-auto d-block" />
                        <h3>High-Quality</h3>
                        <h3>Groceries</h3>
                        <p3>You can shop for fresh groceries yourself through the optimal route.</p3>
                    </div>
                </div>
            </div>
            {/* <div className="targetImage2">
                <img className="targetImage" src="img/target.png" ></img>
            </div> */}
        </div>
    );
}

export default InfoSection;