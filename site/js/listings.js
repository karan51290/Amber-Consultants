(function () {
  "use strict";

  // Both values are public/non-secret, safe to hardcode — the security
  // boundary is Sanity's read-only CDN API itself, not these identifiers.
  var SANITY_PROJECT_ID = "ortbv0xn";
  var SANITY_DATASET = "production";
  var SANITY_API_VERSION = "2024-01-01";

  // Sourced from business.json via the generated js/business-config.js
  // (loaded before this script on every page); falls back if that's missing.
  var BIZ = window.AMBER_BUSINESS || {};
  var WHATSAPP_NUMBER = BIZ.whatsappNumber || "919677195239";

  var QUERY = '*[_type == "listing" && status == "available"] | order(featured desc, publishedAt desc){' +
    "title, slug, price, priceLabel, locality, propertyType, bedrooms, bathrooms, areaSqft, images, featured" +
    "}";

  function apiUrl(query) {
    var base = "https://" + SANITY_PROJECT_ID + ".apicdn.sanity.io/v" + SANITY_API_VERSION +
      "/data/query/" + SANITY_DATASET;
    return base + "?query=" + encodeURIComponent(query);
  }

  // Sanity image asset refs are self-describing: "image-<id>-<w>x<h>-<format>",
  // so a card image URL can be built without a second dereferencing query.
  function imageUrl(assetRef, width) {
    var parts = assetRef.split("-");
    var id = parts[1];
    var dimensions = parts[2];
    var format = parts[3];
    return "https://cdn.sanity.io/images/" + SANITY_PROJECT_ID + "/" + SANITY_DATASET + "/" +
      id + "-" + dimensions + "." + format + "?w=" + width + "&auto=format&fit=crop";
  }

  function escapeHtml(str) {
    var div = document.createElement("div");
    div.textContent = str == null ? "" : String(str);
    return div.innerHTML;
  }

  function formatPrice(listing) {
    if (listing.priceLabel) return listing.priceLabel;
    if (typeof listing.price === "number") return "₹" + listing.price.toLocaleString("en-IN");
    return "";
  }

  function whatsappLink(listing) {
    var text = "Hi Amber Consultants, I'm interested in \"" + listing.title + "\"" +
      (listing.locality ? " (" + listing.locality + ")" : "") + ". Could you share more details?";
    return "https://api.whatsapp.com/send/?phone=" + WHATSAPP_NUMBER + "&text=" + encodeURIComponent(text);
  }

  function factsLine(listing) {
    var facts = [];
    if (listing.bedrooms) facts.push(listing.bedrooms + " Bed");
    if (listing.bathrooms) facts.push(listing.bathrooms + " Bath");
    if (listing.areaSqft) facts.push(listing.areaSqft + " sqft");
    return facts.join(" · ");
  }

  function cardHtml(listing) {
    var img = listing.images && listing.images[0] && listing.images[0].asset
      ? imageUrl(listing.images[0].asset._ref, 480)
      : "";
    var facts = factsLine(listing);

    return (
      '<article class="listing-card">' +
        '<div class="listing-card-media">' +
          (img ? '<img src="' + img + '" alt="' + escapeHtml(listing.title) + '" loading="lazy">' : "") +
        "</div>" +
        '<div class="listing-card-body">' +
          '<h3 class="listing-card-title">' + escapeHtml(listing.title) + "</h3>" +
          (listing.locality ? '<p class="listing-card-locality">' + escapeHtml(listing.locality) + "</p>" : "") +
          (facts ? '<p class="listing-card-facts">' + escapeHtml(facts) + "</p>" : "") +
          '<p class="listing-card-price">' + escapeHtml(formatPrice(listing)) + "</p>" +
          '<a class="btn btn-primary btn-sm" href="' + whatsappLink(listing) + '" target="_blank" rel="noopener">Enquire on WhatsApp</a>' +
        "</div>" +
      "</article>"
    );
  }

  function fetchListings() {
    return fetch(apiUrl(QUERY)).then(function (res) {
      if (!res.ok) throw new Error("Sanity API error: " + res.status);
      return res.json();
    }).then(function (json) {
      return json.result || [];
    });
  }

  function showLoading(visible) {
    var el = document.getElementById("listings-loading");
    if (el) el.hidden = !visible;
  }

  function showEmptyState(visible) {
    var el = document.getElementById("listings-empty-state");
    if (el) el.hidden = !visible;
  }

  function renderListings(listings) {
    var grid = document.getElementById("listings-grid");
    showLoading(false);

    if (!listings.length) {
      showEmptyState(true);
      return;
    }

    showEmptyState(false);
    grid.innerHTML = listings.map(cardHtml).join("");
    grid.hidden = false;
  }

  function showFallback(err) {
    console.error("Failed to load listings:", err);
    showLoading(false);
    showEmptyState(true);
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (!document.getElementById("listings-grid")) return; // only run on listings.html
    fetchListings().then(renderListings).catch(showFallback);
  });
})();
