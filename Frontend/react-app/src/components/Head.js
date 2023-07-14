import React from 'react';

const Head = (props) => {
  return (
    <>
      <div style={{ backgroundColor: 'rgb(209,225,230)' }}>
        <h1 data-testid="h">Welcome to Bullseye</h1>
        <img
          class='bullseye'
          src='img/BullseyeEdited.png'
          width='17%'
          height='17%'
        />
      </div>
    </>
  );
};

export default Head;
