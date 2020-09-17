function hasError(json) {
  if (json.error !== undefined && !json.success) {
  //if (json.success == false) {
    //alert('error');
    console.dir(json.error);
    errorHandler(json.error);
  }
}

function errorHandler(code) {
  let message = '';
  let alert_type = '';
  let logout = false;
  switch(code) {
    case 401:
      alert_type = ' alert-info';
      message = 'Signed out';
      logout = true;
      break;
    case 403:
      alert_type = ' alert-info';
      message = 'Action not allowed';
      logout = true;
      break;
    case 422:
      alert_type = ' alert-danger';
      message = 'Unhandled error';
      break;
    default:
      alert_type = '';
      message = '';
  }

  message = '<div class="alert' + alert_type + '">' + message + '</div>';
  $('#error-msg').html(message);

  if (logout) {
    setTimeout(() => {
      window.location.href='/logout';
    }, 2000);
  }

}