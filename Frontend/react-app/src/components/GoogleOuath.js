import React from 'react';
import { useEffect, useState } from 'react';
import jwt_decode from 'jwt-decode';
import { Link } from 'react-router-dom';
import { authorize } from './Global'
import { useSearchParams, useNavigate } from "react-router-dom";
import './GoogleOuath.css';

function GoogleOuath() {
  const [searchParams, setSearchParams] = useSearchParams();

  function logout() {
    authorize.userLoggedIn = false;
    authorize.userName = null;
    authorize.access_token = null;
    window.location.href = "/Home";
    // searchParams.delete("access_token");
    // searchParams.delete("user_email");
    // setSearchParams(searchParams);
  }

  if (authorize.userLoggedIn === false) {
    return (
      <div>
        <Link to={authorize.LoginRedirectEndpoint}>
          <button className='button-style'>Sign In</button>
        </Link>
      </div>
    );
  } else {
    return (
      <button onClick={logout} className="button-style">Sign Out</button>
    );
  }

}

export default GoogleOuath;

