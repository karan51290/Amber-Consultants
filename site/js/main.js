// Amber Consultants — shared site behavior (mobile nav, dropdown, accordion, gallery lightbox)
document.addEventListener('DOMContentLoaded', function () {

  /* ---- Mobile nav sheet ---- */
  var toggle = document.querySelector('.nav-toggle');
  var backdrop = document.querySelector('.sheet-backdrop');
  function closeNav() { document.body.classList.remove('nav-open'); }
  if (toggle) {
    toggle.addEventListener('click', function () {
      document.body.classList.toggle('nav-open');
    });
  }
  if (backdrop) backdrop.addEventListener('click', closeNav);
  document.querySelectorAll('.mobile-sheet a').forEach(function (a) {
    a.addEventListener('click', closeNav);
  });

  /* ---- Services dropdown: tap-to-open on touch/mobile-width devices ---- */
  document.querySelectorAll('.has-dropdown > .nav-link').forEach(function (link) {
    link.addEventListener('click', function (e) {
      if (window.innerWidth <= 900) return; // mobile sheet renders it inline already
      var parent = link.parentElement;
      var isOpenSomewhereElse = document.querySelector('.has-dropdown.open') !== parent;
      if (isOpenSomewhereElse) {
        e.preventDefault();
        document.querySelectorAll('.has-dropdown.open').forEach(function (el) { el.classList.remove('open'); });
        parent.classList.add('open');
      }
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.has-dropdown')) {
      document.querySelectorAll('.has-dropdown.open').forEach(function (el) { el.classList.remove('open'); });
    }
  });

  /* ---- Accordion ---- */
  document.querySelectorAll('.acc-trigger').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.closest('.acc-item');
      var wasOpen = item.classList.contains('open');
      item.parentElement.querySelectorAll('.acc-item').forEach(function (i) { i.classList.remove('open'); });
      if (!wasOpen) item.classList.add('open');
    });
  });

  /* ---- Gallery lightbox ---- */
  var galleryImgs = Array.prototype.map.call(document.querySelectorAll('.gallery-item img'), function (img) { return img; });
  var lightbox = document.querySelector('.lightbox');
  if (lightbox && galleryImgs.length) {
    var lbImg = lightbox.querySelector('img');
    var currentIndex = 0;

    function show(i) {
      currentIndex = (i + galleryImgs.length) % galleryImgs.length;
      lbImg.src = galleryImgs[currentIndex].src;
      lbImg.alt = galleryImgs[currentIndex].alt || '';
    }
    galleryImgs.forEach(function (img, i) {
      img.closest('.gallery-item').addEventListener('click', function () {
        show(i);
        lightbox.classList.add('open');
      });
    });
    lightbox.querySelector('.lightbox-close').addEventListener('click', function () {
      lightbox.classList.remove('open');
    });
    lightbox.querySelector('.lightbox-prev').addEventListener('click', function () { show(currentIndex - 1); });
    lightbox.querySelector('.lightbox-next').addEventListener('click', function () { show(currentIndex + 1); });
    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox) lightbox.classList.remove('open');
    });
    document.addEventListener('keydown', function (e) {
      if (!lightbox.classList.contains('open')) return;
      if (e.key === 'Escape') lightbox.classList.remove('open');
      if (e.key === 'ArrowRight') show(currentIndex + 1);
      if (e.key === 'ArrowLeft') show(currentIndex - 1);
    });
  }

  /* ---- Sends a form's fields to WhatsApp as a pre-filled message ---- */
  function sendToWhatsApp(text) {
    var waNumber = (window.AMBER_BUSINESS && window.AMBER_BUSINESS.whatsappNumber) || '919677195239';
    window.open('https://api.whatsapp.com/send/?phone=' + waNumber + '&text=' + encodeURIComponent(text), '_blank', 'noopener');
  }

  /* ---- Contact form: compose a WhatsApp message with the entered details ---- */
  var contactForm = document.querySelector('#contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = contactForm.name.value.trim();
      var email = contactForm.email.value.trim();
      var phone = contactForm.phone.value.trim();
      var message = contactForm.message.value.trim();
      sendToWhatsApp(
        'Hi Amber Consultants, my name is ' + name + '.\n' +
        'Phone: ' + phone + '\n' +
        (email ? 'Email: ' + email + '\n' : '') +
        '\n' + message
      );
    });
  }

  /* ---- Sell/Rent form: compose a WhatsApp message with the entered details ---- */
  var sellForm = document.querySelector('#sell-form');
  if (sellForm) {
    sellForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = sellForm.name.value.trim();
      var phone = sellForm.phone.value.trim();
      var locality = sellForm.locality.value.trim();
      var category = sellForm.category.value;
      var price = sellForm.price.value.trim();
      var description = sellForm.description.value.trim();
      sendToWhatsApp(
        "Hi Amber Consultants, I'd like to " + category.toLowerCase() + ' my property.\n' +
        'Name: ' + name + '\n' +
        'Phone: ' + phone + '\n' +
        'Location: ' + locality + '\n' +
        (price ? 'Expected Price/Rent: ' + price + '\n' : '') +
        (description ? '\n' + description : '')
      );
    });
  }
});
