const backend_url = "https://api.bullseye.host";

const authorize = {
  LoginRedirectEndpoint: `${backend_url}/auth/login-redirect`,
  userLoggedIn: false,
  userName: null,
  access_token: null,
  email: null,
};

export { authorize, backend_url };
