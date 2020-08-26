/* 
From Udacity coffe shop
*/
const JWTS_LOCAL_KEY = 'JWTS_LOCAL_KEY';


function active_jwt(){
  return localStorage.getItem(JWTS_LOCAL_KEY);
}

function set_jwt(token) {
  localStorage.setItem(JWTS_LOCAL_KEY, token);
}

function decode_jwt() {
  let payload = "";
  let token = localStorage.getItem(JWTS_LOCAL_KEY) || null;
  if (token) {
    payload = parseJwt(token);
  }
  return payload;
}

function logout() {
  set_jwt("");
  window.location.href = "/logout";
}


/*
https://stackoverflow.com/questions/38552003/how-to-decode-jwt-token-in-javascript-without-using-a-library
*/
function parseJwt (token) {
  var base64Url = token.split('.')[1];
  var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));

  return JSON.parse(jsonPayload);
};
