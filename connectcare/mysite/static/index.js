$(function() {
  $('<img/>').attr('src', 'http://lorempixel.com/1400/900/nature/3').load(function() {
    $('.bg-img').append($(this));
    // simulate loading
    setTimeout(function() {
     $('.container').addClass('loaded');
    }, 1500)
   //$(this).remove(); // prevent memory leaks as @benweet suggested
  });
  $('.form-toggle').on('click', function() {
    $('.container').toggleClass('show-register')
  })
})