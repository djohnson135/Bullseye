/*global chrome*/
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Avatar from 'react-avatar';
import Alert from 'react-bootstrap/Alert';
import React, { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner';

/**
 * Simulates a network request for loading and showing purposes
 * @returns {Promise}
 */
function simulateNetworkRequest() {
  return new Promise((resolve) => setTimeout(resolve, 2000));
}
/**
 * Function that calls the POPUP listener from background.js in order to run the content script that will get the information from the target shopping page. Utilizes the chrome.extension API's chrome.runtime system.
 */
function message() {
  setTimeout(() => {
    chrome.runtime.sendMessage({ greeting: "POPUP" }, function (response) {
      console.log(response.farewell);
    });
  }, 3000);
}

/**
 * This react element provides the user the ability to see that they are logged in, view our logo through an image, click the Generate Path button to generate their shopping path once on the Target page, and link them to the map once it is generated.
 * To get the user information, the handleGetProfile function is utilized from background.js.
 * Once the Generate Path button is called, the function message is called, which utilizes the chrome.extension api to set up a message/listener with background.js where the logic to get the necessary information is written.
 * Various react elements, html, and css styling are utlized in the design of the popup.
 * @returns App: react element of the Chrome Extension popup
 */
function App() {
  const [show, setShow] = useState(false);
  const [isLoading, setLoading] = useState(false);
  const [loadingComplete, setComplete] = useState(false);
  const [name, setName] = useState("");
  const [imageURL, setImageURL] = useState("");
  const handleClick = () => setLoading(true);

  useEffect(() => {
    if (isLoading) {
      simulateNetworkRequest().then(() => {
        setLoading(false);
        setShow(true);
        setComplete(true);
      });
    }
  }, [isLoading]);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await chrome.runtime.sendMessage("get-user-profile");
        setName(response.name);
        setImageURL(response.picture);
      } catch (err) {
        console.log(err.message);
        setName("Jane Doe");
        setImageURL("http://www.gravatar.com/avatar");
      }
    };
    fetchUser();
  }, []);

  return (
    <div>
      <div>
        <h1 class="header">Bullseye <span class="red">for Chrome</span>
          <a href="https://google.com" target="_blank" rel="noreferrer">
            <img class="wheel" src="img/information.png" />
          </a>
        </h1>
      </div>

      <center>
        <hr class="line" />
      </center>

      <div class="container">
        <img class="bullseye" src="img/Bullseye.png" />
        <div class="inner1">
          <Avatar size="80" round={true} src={imageURL} />
          <div class="name">
            {name}
          </div>
        </div>
      </div>

      <center>
        <Button
          onClick={() => {
            handleClick()
            message()
          }}
          className="button1"
          variant="danger"
          disabled={loadingComplete || isLoading}
        >
          {isLoading ? 'Loading' : 'Generate Path From Cart'}
          &nbsp;
          {isLoading === true && <Spinner animation="border" variant="light" size="sm" />}
        </Button>

        <Alert show={show} variant="warning">
          <Alert.Heading>Your path was generated.</Alert.Heading>
          <p class="alertFont">
            Here is a link : &nbsp;
            <span>
              <a href="https://www.bullseye.host/Home" target="_blank" rel="noreferrer">
                www.bullseye.host
              </a>
            </span>
          </p>
          <hr />
          <Button
            onClick={() => {
              setShow(false)
              setComplete(false)
            }}
            variant="outline-secondary"
            size="sm">
            Close
          </Button>
        </Alert>
      </center>
    </div>
  );
}

export default App;

