function addtocart(href_url) {


  axios({
    method: 'post',
    url: href_url,
    data: {
    },
    headers: {
      'X-CSRFToken': csrftoken,
    },
    dataType: 'json',
  })


}


function removeFromcart(href_url) {

  axios({
    method: 'post',
    url: href_url,
    data: {
    },
    headers: {
      'X-CSRFToken': csrftoken,
    },
    dataType: 'json',
  })


}
var i = 0;

function incrementcart(href_url) {
  // i++;
  // document.getElementById('cartCounter').innerHTML = i;


  axios({
    method: 'post',
    url: href_url,
    data: {
    },
    headers: {
      'X-CSRFToken': csrftoken,
    },
    dataType: 'json',
  })


}

function decremnentcart(href_url) {

  axios({
    method: 'post',
    url: href_url,
    data: {
    },
    headers: {
      'X-CSRFToken': csrftoken,
    },
    dataType: 'json',
  })


}