$(function () { function e() { s.addClass("overflow-hidden"), o.show(), setTimeout(function () { s.addClass("side-menu-visible"), d.fadeIn() }, 50) } function n() { s.removeClass("side-menu-visible"), d.fadeOut(), setTimeout(function () { o.hide(), s.removeClass("overflow-hidden") }, 400) } var s = $("body"), i = $(".navbar"), a = $(".navbar-collapse"); s.append('<div class="side-menu-overlay"></div>'); var d = $(".side-menu-overlay"); s.append('<div id="side-menu"></div>'); var o = $("#side-menu"); o.append('<button class="close"><span aria-hidden="true">×</span></button>'); var t = o.find(".close"); o.append('<div class="contents"></div>'); var l = o.find(".contents"); i.hasClass("better-bootstrap-nav-left") && o.addClass("side-menu-left"), a.on("show.bs.collapse", function (n) { n.preventDefault(); var s = $(this).html(); l.html(s), e() }), t.on("click", function (e) { e.preventDefault(), n() }), d.on("click", function (e) { n() }), $(window).resize(function () { !a.is(":visible") && s.hasClass("side-menu-visible") ? (o.show(), d.show()) : (o.hide(), d.hide()) }) });






$(document).ready(function () {

  //Check to see if the window is top if not then display button
  $(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
      $('.scrollToTop').fadeIn();
    } else {
      $('.scrollToTop').fadeOut();
    }
  });

  //Click event to scroll to top
  $('.scrollToTop').click(function () {
    $('html, body').animate({ scrollTop: 0 }, 800);
    return false;
  });

});




$('.carousel').carousel({
  interval: 6000,
  pause: false,
});



$(window).on('load', function () {
  $("body").css("overflow", "auto");
  $(".loadingPage").fadeOut(1000);

});




jQuery('.quantity').each(function () {
  var spinner = jQuery(this),
    input = spinner.find('input[type="number"]'),
    btnUp = spinner.find('.quantity-up'),
    btnDown = spinner.find('.quantity-down'),
    min = input.attr('min'),
    max = input.attr('max');

  btnUp.click(function () {
    var oldValue = parseFloat(input.val());
    if (oldValue >= max) {
      var newVal = oldValue;
    } else {
      var newVal = oldValue + 1;
    }
    spinner.find("input").val(newVal);
    spinner.find("input").trigger("change");
  });

  btnDown.click(function () {
    var oldValue = parseFloat(input.val());
    if (oldValue <= min) {
      var newVal = oldValue;
    } else {
      var newVal = oldValue - 1;
    }
    spinner.find("input").val(newVal);
    spinner.find("input").trigger("change");
  });

});






/* Set rates + misc */
var taxRate = 0.05;
var shippingRate = 15.00;
var fadeTime = 300;


/* Assign actions */
$('.product-quantity input').change(function () {
  updateQuantity(this);
});

$('.product-removal button').click(function () {
  removeItem(this);
});


/* Recalculate cart */

$(document).ready(function recalculateCart() {



  var subtotal = 0;

  /* Sum up row totals */
  $('.product').each(function () {
    subtotal += parseFloat($(this).children('.product-line-price').text());
  });

  /* Calculate totals */
  var tax = subtotal * taxRate;
  var shipping = (subtotal > 0 ? shippingRate : 0);
  var total = subtotal;

  /* Update totals display */
  $('.totals-value').fadeOut(fadeTime, function () {

    $('#cart-total').html(total.toFixed(2));
    if (total == 0) {

      $('.checkout').fadeOut(fadeTime);
    } else {
      $('.checkout').fadeIn(fadeTime);
    }
    $('.totals-value').fadeIn(fadeTime);
  });
});




function recalculateCart() {
  var subtotal = 0;

  /* Sum up row totals */
  $('.product').each(function () {
    subtotal += parseFloat($(this).children('.product-line-price').text());
  });

  /* Calculate totals */
  var tax = subtotal * taxRate;
  var shipping = (subtotal > 0 ? shippingRate : 0);
  var total = subtotal;

  /* Update totals display */
  $('.totals-value').fadeOut(fadeTime, function () {

    $('#cart-total').html(total.toFixed(2));
    if (total == 0) {
      $('.checkout').fadeOut(fadeTime);
    } else {
      $('.checkout').fadeIn(fadeTime);
    }
    $('.totals-value').fadeIn(fadeTime);
  });
}


/* Update quantity */
function updateQuantity(quantityInput) {
  /* Calculate line price */
  var productRow = $(quantityInput).parent().parent();
  var price = parseFloat(productRow.children('.product-price').text());
  var quantity = $(quantityInput).val();
  var linePrice = price * quantity;

  /* Update line price display and recalc cart totals */
  productRow.children('.product-line-price').each(function () {
    $(this).fadeOut(fadeTime, function () {
      $(this).text(linePrice.toFixed(2));
      recalculateCart();
      $(this).fadeIn(fadeTime);
    });
  });
}


/* Remove item from cart */
function removeItem(removeButton) {
  /* Remove row from DOM and recalc cart total */
  var productRow = $(removeButton).parent().parent();
  productRow.slideUp(fadeTime, function () {
    productRow.remove();
    recalculateCart();
  });
}




$(".owl-carousel").owlCarousel({
  loop: true,
  margin: 20,
  autoplay: true,
  autoplayTimeout: 2500,
  dots: true,
  smartSpeed: 1500,
  responsive: {
    0: {
      items: 1
    },
    350: {
      items: 2
    },
    500: {
      items: 3
    },
    650: {
      items: 4
    },
    901: {
      items: 5
    },

    1200: {
      items: 6
    },

  }
});



var count = 0;
$('.addToCartButton').on('click', function () {
  count += 1;
  var $button = $(this);
  $button.addClass('state-change');
  $button.addClass('loading-state');
  setTimeout(function () {
    $button.removeClass('loading-state');
  }, 300);

  setTimeout(function () {
    $button.addClass('success-state');
    setTimeout(function () {
      $button.removeClass('success-state');
    }, 1000);
  }, 800);

  setTimeout(function () {
    setTimeout(function () {
      $button.removeClass('state-change')
    }, 1000)
  }, 800);

});