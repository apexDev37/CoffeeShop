/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

// Load environment variables
// Enter Auth0 developer credentials in auth0 object


export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: '', // the auth0 domain prefix
    audience: '', // the audience set for the auth0 app
    clientId: '', // the client id generated for the auth0 app
    callbackURL: 'https://127.0.0.1:8100', // the base url of the running ionic application. 
  }
};
