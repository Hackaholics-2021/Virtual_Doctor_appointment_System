var settings = {
    "url": "http://127.0.0.1:5000/users",
    "method": "GET",
    "timeout": 0,
  };
  
  $.ajax(settings).done(function (response) {
    console.log(response);
    document.getElementById("first").innerHTML = response["data"]
  });